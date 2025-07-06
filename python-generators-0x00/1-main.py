#!/usr/bin/python3
from itertools import islice

mod = __import__('0-stream_users')       # ✅ import the module
stream_users = mod.stream_users          # ✅ get the function from it

for user in islice(stream_users(), 6):
    print(user)
