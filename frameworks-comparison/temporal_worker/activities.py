import asyncio
from temporalio import activity

@activity.defn
async def do_work(x: int) -> int:
    await asyncio.sleep(0.05)
    return x
