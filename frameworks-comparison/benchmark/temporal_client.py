import asyncio
import logging
import os
import time
from datetime import timedelta

from temporalio.client import Client

TEMPORAL_ADDRESS = os.getenv("TEMPORAL_ADDRESS", "temporal:7233")
TEMPORAL_NAMESPACE = os.getenv("TEMPORAL_NAMESPACE", "default")
TASK_QUEUE = os.getenv("TASK_QUEUE", "benchmark-task-queue")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
async def run_temporal_once(n: int) -> int:
    logging.info(f"[temporal] TEMPORAL_ADDRESS={TEMPORAL_ADDRESS}, NAMESPACE={TEMPORAL_NAMESPACE}")
    logging.info(f"[temporal] Running temporal client for {n} tasks")
    start = time.perf_counter()
    client = await Client.connect(TEMPORAL_ADDRESS)
    logging.info(f"Client connected to {TEMPORAL_ADDRESS}")
    result = await client.execute_workflow(
        "BenchmarkWorkflow",
        n,
        id=f"benchmark-temporal_worker-{int(start*1000)}",
        task_queue=TASK_QUEUE,
        run_timeout=timedelta(seconds=10),
        task_timeout=timedelta(seconds=5)
    )
    logging.info(result)
    return result
