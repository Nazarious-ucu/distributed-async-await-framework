import time
import asyncio
from client import pick, Resonate

class TestHarness:
    def __init__(self, num_jobs: int = 10, job_duration: int = 20):
        self.num_jobs = num_jobs
        self.job_duration = job_duration
        self.results = []

    def run_baseline(self):
        """Baseline test: normal execution"""
        start = time.time()
        for i in range(self.num_jobs):
            job_id = f"baseline-{i}"
            res = (
                pick(job_id)
                .options(target="poll://any@workers")
                .rpc(f"job-{hash(job_id)}", "long_job", job_id, self.job_duration)
            )
            elapsed = time.time() - start
            self.results.append({"job_id": job_id, "elapsed": elapsed, "result": res})

        return self.results

    def print_summary(self):
        print(f"\n=== Test Summary ===")
        print(f"Total jobs: {len(self.results)}")
        print(f"Total time: {self.results[-1]['elapsed']:.2f}s")
        print(f"Avg job time: {sum(r['elapsed'] for r in self.results) / len(self.results):.2f}s")

if __name__ == "__main__":
    harness = TestHarness(num_jobs=5, job_duration=20)
    harness.run_baseline()
    harness.print_summary()

