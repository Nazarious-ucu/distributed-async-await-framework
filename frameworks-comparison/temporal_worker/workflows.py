from datetime import timedelta

from temporalio import workflow
import activities
@workflow.defn
class BenchmarkWorkflow:
    @workflow.run
    async def run(self, n: int) -> int:

        total = 0
        for _ in range(n):
            value = await workflow.execute_activity(
                activities.do_work,
                1,
                schedule_to_close_timeout=timedelta(seconds=10),
            )
            total += value
        return total
