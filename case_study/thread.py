from concurrent.futures.thread import ThreadPoolExecutor

"""The `concurrent.futures` module is part of Python's standard library and provides a high-level
interface for asynchronously executing callabels. 
The `ThreadPoolExecutor` class is an Executor subclass that uses a pool of threads to execute calls asynchronously.
"""

def task(n):
    if n == 0:
        raise ValueError("n must not be zero")
    return 10/n

# Create a ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = {executor.submit(task, n) for n in range(5)}
    for future in futures:
        try:
            result = future.result()
            print(result)
        except ValueError as e:
            print(f"Caught an exception: {e}")
    