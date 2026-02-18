from resonate import Resonate

r1 = Resonate.remote(group="client", host="http://localhost", store_port="8001", message_source_port="8002")
r2 = Resonate.remote(group="client", host="http://localhost", store_port="8003", message_source_port="8004")

def pick(job_id: str):
    return r1 if (hash(job_id) % 2 == 0) else r2

def main():
    for job_id in ["a", "b", "c", "d"]:
        res = (
            pick(job_id)
            .options(target="poll://any@workers")
            .rpc(f"job-{hash(job_id)}", "long_job", job_id, 20)
        )
        print(job_id, res)

if __name__ == "__main__":
    main()
