from dataclasses import dataclass

import numpy as np


@dataclass
class SymGradient:
    gradient: np.ndarray
    fnorm: float
    snorm: float
    converged: bool
    backF_av: np.ndarray
    backS_vv: np.ndarray
    symmetry_force_violation: float
    symmetry_stress_violation: float
    volume: float

    def loginfo(self):
        return {
            'F': self.fnorm,
            'S': self.snorm,
            'Ferr': self.symmetry_force_violation,
            'Serr': self.symmetry_stress_violation,
            'V': self.volume,
        }

    def datafy(self):
        # XXX save something useful
        return {}


class SymOpt:
    iotype = 'symopt'

    def __init__(self, symmatoms, fmax, smax):
        self.symmatoms = symmatoms
        self.fmax = symmatoms.fmax = fmax
        self.smax = symmatoms.smax = smax

    def step_to_string(self, step):
        return self.symmatoms.step_to_string(
            step.i, self.fmax, self.smax, step.gradient_obj
        )

    def log_headers(self):
        return self.symmatoms.logheaders()

    @property
    def optimizable(self):
        # Needed for gradient_norm()
        return self.symmatoms

    def datafy(self):
        # What do we need to save?
        # symmatoms defines the initial reduced positions as 0, so the
        # mapping absolutely needs saving aside from the Hessian.
        return {}  # XXX

    @classmethod
    def undatafy(cls, dct):
        raise NotImplementedError

    @classmethod
    def undatafy_gradient(cls, dct):
        raise NotImplementedError

    def get_value(self):
        return self.symmatoms.get_value()

    def get_gradient(self):
        return self.symmatoms._get_gradient()

        # def loginfo():
        #     return {'hello': 42}

        # return SymGradient(**gradient)

    def get_x(self):
        return self.symmatoms.get_x()

    def set_x(self, x):
        self.symmatoms.set_x(x)

    def initial_hessian(self):
        raise NotImplementedError

    def iterimages(self):
        yield self.symmatoms.actual_atoms
