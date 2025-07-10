def firstn(n):
    num = 0
    while num < n:
        yield num
        num += 1

number = firstn(10)
print(number)
squares = (x * x for x in range(10))

#simple decorator
def decorator(func):
    def wrapper():
        print("Before function call")
        func()
        print("After function call")
    return wrapper

@decorator
def say_hello():
    print("Hello!")

#decorator with argument
def do_twice(func):
    def wrapper_do_twice(*args, **kwargs):
        func(*args, **kwargs)
        func(*args, **kwargs)
    return wrapper_do_twice

@do_twice
def greet(name):
    print(f"Hello {name}")
name = 'Emmanuel'
print(greet(name))

import asyncio

async def greet(name):
    print(f"Hello {name}")
    await asyncio.sleep(3)
    print(f"Goodbye {name}")

asyncio.run(greet("World"))

async def main():
    await asyncio.gather(
        greet("Alice"),
        greet("Bob"),
    )

asyncio.run(main())