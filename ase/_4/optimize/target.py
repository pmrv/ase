from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np
from scipy.sparse import eye_array, sparray

from ase import Atoms
from ase.optimize.optimize import OptimizableAtoms
from ase.utils.abc import Optimizable


@dataclass
class ForceGradient:
    gradient: np.ndarray
    forces: np.ndarray
    fnorm: float
    converged: bool

    def loginfo(self) -> dict[str, float]:
        return {'fmax': self.fnorm}


class BaseTarget(ABC):
    def __init__(self, *args, **kwargs) -> None:
        self.optimizable: Optimizable

    @abstractmethod
    def get_value(self) -> float: ...

    @abstractmethod
    def get_gradient(self) -> ForceGradient: ...

    @abstractmethod
    def get_x(self) -> np.ndarray: ...

    @abstractmethod
    def set_x(self, x: np.ndarray) -> None: ...

    @abstractmethod
    def initial_hessian(self, *args, **kwargs) -> np.ndarray: ...

    @abstractmethod
    def initial_inverse_hessian(self, *args, **kwargs) -> sparray: ...


class Target(BaseTarget):
    def __init__(self, atoms: Atoms, fmax: float):
        self.optimizable: OptimizableAtoms = atoms.__ase_optimizable__()
        self.fmax = fmax

    def get_value(self) -> float:
        return self.optimizable.get_value()

    def get_gradient(self) -> ForceGradient:
        forces = self.optimizable.atoms.get_forces()
        gradient = -forces.ravel()
        fnorm = get_maxforce(forces)
        converged = fnorm < self.fmax
        return ForceGradient(
            gradient=gradient,
            forces=forces,
            fnorm=fnorm,
            converged=converged,
        )

    def get_x(self) -> np.ndarray:
        return self.optimizable.get_x()

    def set_x(self, x: np.ndarray) -> None:
        self.optimizable.set_x(x)

    def initial_hessian(self, alpha: float = 70.0) -> np.ndarray:
        return initial_position_hessian(self.optimizable.ndofs(), alpha)

    def initial_inverse_hessian(self, alpha: float = 70.0) -> sparray:
        return initial_inverse_position_hessian(self.optimizable.ndofs(), alpha)


def get_maxforce(forces: np.ndarray) -> float:
    return np.linalg.norm(forces, axis=1).max()


def initial_position_hessian(ndofs: int, alpha: float = 70.0) -> np.ndarray:
    return np.diag(np.full(ndofs, 70.0))


def initial_inverse_position_hessian(
    ndofs: int,
    alpha: float = 70.0,
) -> sparray:
    return 1.0 / alpha * eye_array(ndofs, format='coo')
