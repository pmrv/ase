from dataclasses import dataclass
from typing import Callable

import numpy as np


@dataclass
class SymGradient:
    gradient: np.ndarray
    loginfo: Callable
    converged: bool
    Fback_av: np.ndarray
    Sback_vv: np.ndarray


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
        gradient = self.symmatoms.get_gradient()
        converged = self.symmatoms.converged(gradient, self.fmax)

        def loginfo():
            return {'hello': 42}

        return SymGradient(gradient, loginfo=loginfo, converged=converged)

    def get_x(self):
        return self.symmatoms.get_x()

    def set_x(self, x):
        self.symmatoms.set_x(x)

    def initial_hessian(self):
        raise NotImplementedError

    def iterimages(self):
        raise NotImplementedError
