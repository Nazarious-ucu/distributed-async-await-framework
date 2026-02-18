import signal
from resonate import Resonate, Context

resonate = Resonate.remote(
    group="workers",
    host="http://localhost",
    store_port="8003",
    message_source_port="8004",
)

@resonate.register
def long_job(ctx: Context, job_id: str, seconds: int = 20) -> str:
    for i in range(seconds):
       print(f"job_id: {job_id}, step: {str(i)}")
       yield ctx.sleep(1.0)
    return f"done:{job_id}"

if __name__ == "__main__":
    resonate.start()
    print("worker2 up (server2)")
    signal.pause()
