from functools import partial 

# functools module is for higher-order functions, functions that act on or return other functions.
# functools.partial is a function that allows you to fix a certain number of arguments of a function and
# generate a new function

def multiply(x, y):
    return x * y

# Create a new function that multiplies by 2
double = partial(multiply, 2)

print(double(4))