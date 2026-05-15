from ase._4.atoms import Atoms
from ase._4.calculators.calculator import BaseCalculator
from ase.calculators.calculator import PropertyNotImplementedError


class PotentialEnergySurface:
    """Caches and manages evaluations of atoms.

    Used by geometry optimisation, molecular dynamics, and
    similar, wherever caching is required.

    Operations that invalidate the cache (e.g., setting atoms'
    positions) must be set via PotentialEnergySurface methods
    (e.g., pes.set_positions) and not directly
    (NOT atoms.set_positions).

    DEV: Requested properties need to be defined at initialization,
         but we might want to rethink this.

    """

    def __init__(
        self,
        atoms: Atoms,
        calc: BaseCalculator,
        requested_properties: tuple[str, ...] | None = None,
    ):
        """Initialize the potential energy surface.

        Parameters
        ----------
        atoms: Atoms
            Atomic configuration to evaluate.
        calc: BaseCalculator
            Calculator used to compute properties of ``atoms``.
        requested_properties: tuple of str, optional
            Properties to request from ``calc`` on each evaluate().
            Defaults to ``('free_energy', 'forces')`` if the calculator
            implements ``free_energy``, otherwise ``('energy', 'forces')``.
        """
        self.atoms = atoms
        self.calc = calc
        if requested_properties is None:
            if 'free_energy' in calc.implemented_properties:
                requested_properties = ('free_energy', 'forces')
            else:
                requested_properties = ('energy', 'forces')
        self.requested_properties = tuple(requested_properties)
        unsupported = set(self.requested_properties) - set(
            calc.implemented_properties
        )
        if unsupported:
            raise ValueError(
                f'requested_properties {sorted(unsupported)} not in '
                f'calc.implemented_properties '
                f'{sorted(calc.implemented_properties)}'
            )
        self._results = None
        self._stale = True

    def evaluate(self):
        if self._stale:
            self._results = self.calc.evaluate(
                self.atoms, properties=list(self.requested_properties)
            )
            self._stale = False
        return self._results

    def invalidate(self):
        self._stale = True

    def get_positions(self):
        return self.atoms.get_positions()

    def set_positions(self, x):
        """Assumes x is positions-shaped. Invalidates the cache."""
        self.atoms.set_positions(x)
        self.invalidate()

    def get_property(self, prop):
        results = self.evaluate()
        if prop not in results.properties:
            raise PropertyNotImplementedError(
                f'Tried to get {prop} which has not been evaluated. '
                f'Available properties are {list(results.properties.keys())}.'
            )
        return results.properties[prop]
