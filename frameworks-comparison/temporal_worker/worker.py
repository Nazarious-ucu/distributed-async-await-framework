import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

import config
import activities
import workflows

async def main() -> None:
    client = await Client.connect(config.TEMPORAL_ADDRESS, namespace=config.TEMPORAL_NAMESPACE)
    worker = Worker(
        client,
        task_queue=config.TASK_QUEUE,
        workflows=[workflows.BenchmarkWorkflow],
        activities=[activities.do_work],
    )
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
