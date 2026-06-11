from abc import ABC, abstractmethod

import numpy as np
from scipy.sparse import sparray

from ase._4.optimize.run import ForceGradient
from ase.utils.abc import Optimizable


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
