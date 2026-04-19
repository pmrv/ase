from ase._4.atoms import Atoms
from ase._4.calculators.calculator import BaseCalculator
from ase.utils.abc import Optimizable


class PotentialEnergySurface(Optimizable):
    def __init__(
        self,
        atoms: Atoms,
        calc: BaseCalculator,
        properties: tuple[str, ...] | None = None,
    ):
        self.atoms = atoms
        self.calc = calc
        if properties is None:
            if 'free_energy' in calc.implemented_properties:
                properties = ('free_energy', 'forces')
            else:
                properties = ('energy', 'forces')
        self.properties = tuple(properties)
        self._results = None
        self._stale = True

    def evaluate(self):
        if self._stale:
            self._results = self.calc.evaluate(
                self.atoms, properties=list(self.properties)
            )
            self._stale = False
        return self._results

    def invalidate(self):
        self._stale = True

    def get_x(self):
        return self.atoms.get_positions().ravel()

    def set_x(self, x):
        self.atoms.set_positions(x.reshape(-1, 3))
        self.invalidate()

    def get_gradient(self):
        return -self.evaluate().properties['forces'].ravel()

    def get_value(self):
        props = self.evaluate().properties
        return props.get('free_energy', props['energy'])

    def iterimages(self):
        return self.atoms.iterimages()

    def ndofs(self):
        return 3 * len(self.atoms)
