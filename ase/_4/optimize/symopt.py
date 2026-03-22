from dataclasses import dataclass
from typing import Callable

import numpy as np


@dataclass
class SymGradient:
    gradient: np.ndarray
    loginfo: Callable
    converged: bool
    backF_av: np.ndarray
    backS_vv: np.ndarray
    symmetry_force_violation: float
    symmetry_stress_violation: float


class SymOpt:
    iotype = 'symopt'

    def __init__(self, symmatoms, fmax, smax):
        self.symmatoms = symmatoms
        self.fmax = symmatoms.fmax = fmax
        self.smax = symmatoms.smax = smax

    @property
    def optimizable(self):
        # Needed for gradient_norm()
        return self.symmatoms

    def datafy(self):
        raise NotImplementedError

    @classmethod
    def undatafy(cls, dct):
        raise NotImplementedError

    @classmethod
    def undatafy_gradient(cls, dct):
        raise NotImplementedError

    def get_value(self):
        return self.symmatoms.get_value()

    def get_gradient(self):
        gradient = self.symmatoms._get_gradient()

        def loginfo():
            return {'hello': 42}

        return SymGradient(loginfo=loginfo, **gradient)

    def get_x(self):
        return self.symmatoms.get_x()

    def set_x(self, x):
        self.symmatoms.set_x(x)

    def initial_hessian(self):
        raise NotImplementedError

    def iterimages(self):
        raise NotImplementedError
