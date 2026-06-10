from math import sqrt

import pytest

from ase import Atom, Atoms
from ase.calculators.emt import EMT
from ase.constraints import FixAtoms
from ase.io import read
from ase.optimize import (
    BFGS,
    LBFGS,
    BFGSLineSearch,
    LBFGSLineSearch,
)

optclasses = [
    BFGS,
    LBFGS,
    BFGSLineSearch,
    LBFGSLineSearch,
]


@pytest.fixture(name='optcls', params=optclasses)
def fixture_optcls(request):
    optcls = request.param
    return optcls


@pytest.fixture(name='atoms')
def fixture_atoms() -> Atoms:
    # Distance between Cu atoms on a (100) surface:
    d = 3.6 / sqrt(2)
    atoms = Atoms(
        'Cu',
        positions=[(0, 0, 0)],
        cell=(d, d, 1.0),
        pbc=(True, True, False),
    )
    atoms *= (2, 2, 1)  # 2x2 (100) surface-cell

    # Approximate height of Ag atom on Cu(100) surfece:
    h0 = 2.0
    atoms += Atom('Ag', (d / 2, d / 2, h0))

    constraint = FixAtoms(range(len(atoms) - 1))
    atoms.set_constraint(constraint)

    return atoms


@pytest.mark.optimize()
def test_replay(testdir, optcls, atoms):
    atoms.calc = EMT()
    with optcls(atoms, trajectory='AgCu1.traj', logfile='AgCu1.log') as dyn1:
        dyn1.run(fmax=0.1)

    atoms = read('AgCu1.traj')
    atoms.calc = EMT()
    print(atoms.constraints)

    with optcls(atoms, trajectory='AgCu2.traj', logfile='AgCu2.log') as dyn2:
        dyn2.replay_trajectory('AgCu1.traj')
        dyn2.run(fmax=0.01)
