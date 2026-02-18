import asyncio
import logging
import os
import time

from dbos import DBOS
from prometheus_client import start_http_server, Summary, Counter

from temporal_client import run_temporal_once
from resonate_client import run_resonate_once
from app import init_dbos, sum_workflow


TEMPORAL_ADDRESS = os.getenv("TEMPORAL_ADDRESS", "temporal:7233")
TEMPORAL_NAMESPACE = os.getenv("TEMPORAL_NAMESPACE", "default")
TASK_QUEUE = os.getenv("TASK_QUEUE", "benchmark-task-queue")


LATENCY = Summary(
    "framework_latency_seconds",
    "End-to-end latency of benchmark workflow",
    ["framework"],
)
ERRORS = Counter(
    "framework_errors_total",
    "Total errors while running benchmark workflow",
    ["framework"],
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | benchmark | %(levelname)s | %(message)s",
    force=True,
)

def run_dbos_once(n: int) -> int:
    start = time.perf_counter()
    logging.info(f"Starting DBOS {n}")
    try:
        # start_workflow повертає workflow handle
        handle = DBOS.start_workflow(sum_workflow, n)
        # handle.get_result() блокується, поки workflow не завершиться
        result: int = handle.get_result()
        LATENCY.labels("dbos").observe(time.perf_counter() - start)
        return result
    except Exception:
        ERRORS.labels("dbos").inc()
        raise


async def loop_temporal():
    logging.info("Starting temporal loop")
    while True:
        start = time.perf_counter()
        try:
            await run_temporal_once(n=10)
            LATENCY.labels("temporal").observe(time.perf_counter() - start)
        except Exception:
            ERRORS.labels("temporal").inc()
            pass
        await asyncio.sleep(1)

async def loop_resonate():
    logging.info("Starting resonate loop")
    while True:
        start = time.perf_counter()
        try:
            run_resonate_once(n=10)
            LATENCY.labels("resonate").observe(time.perf_counter() - start)
        except Exception:
            ERRORS.labels("resonate").inc()
            pass
        await asyncio.sleep(1)

async def loop_dbos():
    logging.info("Starting DBOS loop")
    while True:
        try:
            run_dbos_once(n=10)
        except Exception:
            pass
        await asyncio.sleep(1)

async def main():
    start_http_server(8000)
    init_dbos()
    LATENCY.labels("smoke").observe(0.123)
    ERRORS.labels("smoke").inc()
    logging.info("Starting benchmark workflow")
    await asyncio.gather(
        loop_temporal(),
        loop_resonate(),
        loop_dbos(),
    )

if __name__ == "__main__":
    asyncio.run(main())
