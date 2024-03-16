# Example of `asyncio.run()`

""" 
asyncio.run() is a function that can be used to execute a coroutine and return the result. It's a high-level call that
sets up the event loop, executes the passed coroutine, and closes the loop. 
"""

import asyncio

async def main():
    print('Hello')
    await asyncio.sleep(1) # 1 second delaying
    print('World')
    
asyncio.run(main())