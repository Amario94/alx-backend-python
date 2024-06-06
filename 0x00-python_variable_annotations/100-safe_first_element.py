#!/usr/bin/env python3

'''
100-safe_first_element.py
'''
from typing import List, Optional, Any

def safe_first_element(lst: List[Any]) -> Optional[Any]:
    '''correct duck-typed annotations
    '''
    if lst:
        return lst[0]
    else:
        return None
