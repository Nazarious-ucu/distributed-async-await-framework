import os

from dbos import DBOS, DBOSConfig

# ---- 1. Init DBOS ----
# https://docs.dbos.dev/python/integrating-dbos

def init_dbos() -> None:
    config: DBOSConfig = {
        "name": "dbos-benchmark",
        "system_database_url": os.environ.get("DBOS_SYSTEM_DATABASE_URL"),
    }
    DBOS(config=config)
    DBOS.launch()

@DBOS.step()
def increment_step(x: int) -> int:
    return x + 1


@DBOS.workflow()
def sum_workflow(n: int) -> int:
    total = 0
    for _ in range(n):
        total = increment_step(total)
    return total
