import ctypes
from typing import List
import numpy as np

library = ctypes.CDLL(r"./Library/target/debug/librust_mlp.dylib")

# Initialize functions
library.create_mlp.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_ubyte]
library.create_mlp.restype = ctypes.c_void_p
library.delete_mlp.argtypes = [ctypes.c_void_p]


def create_mlp(init: List[int], seed: int) -> ctypes.c_void_p:
    # Convert values to C
    array = np.array(init)
    c_list = array.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
    u8_seed = ctypes.c_ubyte(seed)
    return library.create_mlp(c_list, ctypes.c_int(len(array)), u8_seed)


def delete_mlp(ptr: ctypes.c_void_p):
    library.delete_mlp(ptr)

