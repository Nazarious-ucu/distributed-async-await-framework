import signal
from resonate import Resonate, Context

resonate = Resonate.remote(
    group="workers",
    host="http://localhost",
    store_port="8001",
    message_source_port="8002",
)

@resonate.register
def long_job(ctx: Context, job_id: str, seconds: int = 20) -> str:
    for i in range(seconds):
        print(f"job_id: {job_id}, step: {str(i)}")
        yield ctx.sleep(1.0)
    return f"done:{job_id}"

if __name__ == "__main__":
    resonate.start()
    print("worker1 up (server1)")
    signal.pause()
