#!/usr/bin/env python3
'''101-safely_get_value.py
'''

from typing import Any, Dict, TypeVar, Optional

T = TypeVar('T')

def safely_get_value(dct: Dict[Any, Any], key: Any, default: Optional[T] = None) -> Optional[T]:
    '''add type annotations to the function
    '''
    if key in dct:
        return dct[key]
    else:
        return default
