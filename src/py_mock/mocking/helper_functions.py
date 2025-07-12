import random
import uuid
from functools import partial, singledispatch
from string import ascii_letters
from typing import Any

import numpy as np
from numpy import dtypes


@singledispatch
def get_id_func(type_):
    def integer_id():
        return uuid.uuid1().int

    return integer_id


@get_id_func.register
def _(type_: str | np.object_ | dtypes.ObjectDType):
    def string_id():
        return uuid.uuid1().hex

    return string_id


def get_value_func(type_: str, range_: list):
    func: partial[Any]

    if type_.startswith("int"):
        func = partial(random.randint, *range_)
    elif type_.startswith("float"):
        func = partial(random.uniform, *range_)
    elif type_.startswith("object"):
        func = partial(random.choice, ascii_letters)

    return func
