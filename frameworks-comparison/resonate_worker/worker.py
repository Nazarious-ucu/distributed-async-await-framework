import logging
from threading import Event
from typing import Generator, Any

import os
from resonate import Resonate, Context
from config import RESONATE_URL, GROUP

logging.basicConfig(level=logging.DEBUG)
# Connect this worker to the Resonate Server
# Host/ports are taken from env vars: RESONATE_HOST, RESONATE_PORT_STORE, RESONATE_PORT_MESSAGE_SOURCE
resonate = Resonate.remote(group=GROUP, host=RESONATE_URL)

logging.info(f"Resonate: {resonate}")
@resonate.register
def sum_workflow(ctx: Context, n: int) -> Generator[int, Any, int]:
    """
    Very simple durable workflow used only for benchmarking.
    """
    total = 0
    for i in range(n):
        total += i
        # you *could* yield ctx.sleep(0) here, but it's not needed for the benchmark
    return total

@resonate.register
def do_work(ctx, x: int):
    yield ctx.sleep(50)
    return x


def main() -> None:
    resonate.start()

    Event().wait()


if __name__ == "__main__":
    main()
