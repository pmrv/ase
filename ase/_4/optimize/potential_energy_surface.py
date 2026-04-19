from functools import cached_property

from ase._4.atoms import Atoms
from ase._4.calculators.calculator import BaseCalculator
from ase.utils.abc import Optimizable


class PotentialEnergySurface(Optimizable):
    def __init__(self, atoms: Atoms, calc: BaseCalculator):
        self.atoms = atoms
        self.calc = calc

    def get_x(self):
        return self.atoms.get_positions().ravel()

    def set_x(self, x):
        self.atoms.set_positions(x.reshape(-1, 3))

    def get_gradient(self):
        results = self.calc.evaluate(self.atoms, properties=['forces'])
        return -results.properties['forces'].ravel()

    @cached_property
    def _value_property(self):
        if 'free_energy' in self.calc.implemented_properties:
            return 'free_energy'
        return 'energy'

    def get_value(self):
        results = self.calc.evaluate(self.atoms,
                                     properties=[self._value_property])
        return results.properties[self._value_property]

    def iterimages(self):
        return self.atoms.iterimages()

    def ndofs(self):
        return 3 * len(self.atoms)
