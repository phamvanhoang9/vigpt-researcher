# This is an example of how we can use `Generator` from the typing module in Python.

from typing import Generator 

def fibonacci(n: int) -> Generator[int, None, None]:
    a, b = 0, 1
    for _ in range(n):
        yield a # This is the key line that makes this a generator function
        a, b = b, a + b
        # print (a, b)
        
for i in fibonacci(10):
    print(i)