import logging
import time
from datetime import timedelta

from resonate import Resonate

RESONATE_URL = "http://resonate-server"
logging.basicConfig(level=logging.DEBUG)
resonate = Resonate.remote(host=RESONATE_URL, group="invoke")
logging.info("Resonate client started")
def run_resonate_once(n: int) -> int:
    logging.info("Running resonate once")
    try:
        start = time.perf_counter()
        total = 0
        for i in range(n):
            logging.info(f"Running resonate {i}")
            handle = resonate.options(
                target="poll://any@resonate-worker",
                timeout=5
            ).begin_rpc(
                f"bench-{start}-{i}",
                "do_work",
                1,
            )
            logging.info(handle)

            res = handle.result()
            total += res
        return total
    except Exception as e:
        logging.error(e)
        return -1