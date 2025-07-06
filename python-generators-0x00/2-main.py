#!/usr/bin/python3
import sys

mod = __import__('1-batch_processing')  # ✅ import module dynamically
processing = mod                        # ✅ alias

# print processed users in a batch of 50
try:
    for batch in processing.batch_processing(50):
        print(batch)
except BrokenPipeError:
    sys.stderr.close()
