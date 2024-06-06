#!/usr/bin/env python3

'''102-type_checking.py
'''
from typing import List, Tuple

def zoom_array(lst: Tuple[int, ...], factor: int = 2) -> List[int]:
    '''Use mypy to validate the zoom array function
        and return a zoom in list
    '''
    zoomed_in: List[int] = [
        item for item in lst
        for i in range(factor)
    ]
    return zoomed_in

array = (12, 72, 91)  # Using a tuple since the function expects a tuple

zoom_2x = zoom_array(array)

zoom_3x = zoom_array(array, 3)
