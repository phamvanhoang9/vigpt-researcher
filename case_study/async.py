import asyncio
from __future__ import annotations


async def create_chat_completion(messages):
    pass


async def main():
    """Python will "pause" the execution of main until `create_chat_completion` has finished running.
    While `main` is paused, other coroutines can run.
    """
    messages = ["Hello", "How are you?"]
    
    result = await create_chat_completion(messages)
    
asyncio.run(main())