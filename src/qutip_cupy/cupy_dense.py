import cupy as cp
import numbers
from qutip.core import data
class CuPyDense(data.Data):
    def __init__(self, data, shape=None, copy=True):
        base = cp.array(data, dtype=cp.complex128, order='K', copy=copy)
        if shape is None:
            shape = base.shape
            # Promote to a ket by default if passed 1D data.
            if len(shape) == 1:
                shape = (shape[0], 1)
        if not (
            len(shape) == 2
            and isinstance(shape[0], numbers.Integral)
            and isinstance(shape[1], numbers.Integral)
            and shape[0] > 0
            and shape[1] > 0
        ):
            raise ValueError("shape must be a 2-tuple of positive ints, but is " + repr(shape))
        if shape and (shape[0] != base.shape[0] or shape[1] != base.shape[1]):
            if shape[0] * shape[1] != base.size:
                raise ValueError("".join([
                    "invalid shape ",
                    str(shape),
                    " for input data with size ",
                    str(base.size)
                ]))
            else:
                self._cp = base.reshape(shape)
        else:
            
            self._cp = base

        super().__init__((shape[0], shape[1]))

        

def dense_from_cupydense(cupydense):
    
    dense_np = data.Dense(cupydense._cp.tolist())
    return dense_np

def cupydense_from_dense(dense):

    dense_cp = CuPyDense(dense.as_ndarray())
    return dense_cp



