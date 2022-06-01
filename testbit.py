import math
import numpy as np
import pyofdm.codec
import pyofdm.nyquistmodem

get_bin = lambda x, n: format(x, 'b').zfill(n)

a=np.array([10,20,30], dtype=bytearray)
