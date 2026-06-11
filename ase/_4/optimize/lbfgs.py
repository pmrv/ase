import numpy as np

from .method import BaseOptimizationMethod


class LBFGSMethod(BaseOptimizationMethod):
    iotype = 'lbfgs'
    methodname = 'LBFGS'

    def __init__(
        self,
        memory: int = 100,
        alpha: float = 70.0,
    ):
        self.memory = memory
        # Initial approximation of inverse Hessian 1./70. is to emulate the
        # behaviour of BFGS. Note that this is never changed!
        self.H0 = 1.0 / alpha
        self.iteration = 0
        self.s: list[np.ndarray] = []
        self.y: list[np.ndarray] = []
        # Store also rho, to avoid calculating the dot product again and again.
        self.rho: list[float] = []

    def compute_step(self, gradient: np.ndarray) -> np.ndarray:
        loopmax = np.min([self.memory, self.iteration])
        a = np.empty(loopmax, dtype=np.float64)

        q = gradient.copy()
        # ## The algorithm itself:
        for i in range(loopmax - 1, -1, -1):
            a[i] = self.rho[i] * np.dot(self.s[i], q)
            q -= a[i] * self.y[i]
        z = self.H0 * q

        for i in range(loopmax):
            b = self.rho[i] * np.dot(self.y[i], z)
            z += self.s[i] * (a[i] - b)

        self.iteration += 1

        return -z

    def update(
        self,
        pos: np.ndarray,
        gradient: np.ndarray,
        pos0: np.ndarray,
        gradient0: np.ndarray,
    ) -> None:
        s0 = pos - pos0
        self.s.append(s0)

        y0 = gradient - gradient0
        self.y.append(y0)

        rho0 = 1.0 / np.dot(y0, s0)
        self.rho.append(rho0)

        if self.iteration > self.memory:
            self.s.pop(0)
            self.y.pop(0)
            self.rho.pop(0)
