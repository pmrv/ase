from io import StringIO

import numpy as np
import pytest

from ase._4.optimize.bfgs import BFGSMethod, fd_hessian
from ase._4.optimize.run import Optimizer
from ase._4.optimize.symopt import SymOpt
from ase._4.symopt.relax import Relax, SymmetryAdaptedAtoms
from ase.build import fcc111
from ase.calculators.emt import EMT
from ase.filters import FrechetCellFilter
from ase.optimize.bfgs import BFGS
from ase.optimize.cellawarebfgs import CellAwareBFGS
from ase.parallel import world
from ase.utils import spglib_new_errorhandling

symprec = 0.001
fmax = 0.01
smax = 0.0001
ref_energy = 0.4185949


@pytest.fixture
def atoms0():
    return fcc111('Au', size=(1, 1, 2), vacuum=4.0)


@pytest.fixture
def dataset(atoms0):
    import spglib

    dataset = spglib_new_errorhandling(spglib.get_symmetry_dataset)(
        (atoms0.cell, atoms0.get_scaled_positions(), atoms0.numbers),
        symprec=symprec,
    )

    assert dataset.number == 164
    assert len(dataset.rotations) == 12
    return dataset


def test_relaxation_old(atoms0):
    atoms = atoms0.copy()
    target = FrechetCellFilter(
        atoms, mask=[1, 1, 0, 0, 0, 1], exp_cell_factor=1.0
    )
    atoms.calc = EMT()

    buf = StringIO()
    opt = CellAwareBFGS(target, logfile=buf)

    converged = opt.run(fmax=fmax, smax=smax)
    assert converged
    log = buf.getvalue()
    print('LOG')
    print(log)
    for line in log.splitlines():
        if line.startswith('CellAware'):
            nsteps = int(line.split()[1])
    assert nsteps == 7

    energy = atoms.get_potential_energy()
    assert energy == pytest.approx(ref_energy)


def seventy(target):
    ndofs = len(target.get_x())
    return 70.0 * np.identity(ndofs)


@pytest.mark.parametrize(
    'initialize_hessian, nsteps', [(seventy, 7), (fd_hessian, 6)]
)
def test_relaxation_ase4(atoms0, dataset, initialize_hessian, nsteps):
    atoms = atoms0.copy()
    atoms.calc = EMT()

    symmatoms = SymmetryAdaptedAtoms.from_atoms(
        atoms, symprec=symprec, symmorphic=False
    )

    target = SymOpt(symmatoms, fmax=fmax, smax=smax)
    hessian = initialize_hessian(target)

    method = BFGSMethod(hessian)
    opt = Optimizer(target=target, method=method)
    step = opt.run()
    assert step.i == nsteps
    assert step.value == pytest.approx(ref_energy)


def test_relaxation_symopt(atoms0, dataset, tmp_path):
    atoms = atoms0.copy()

    logfile = tmp_path / 'opt.log'

    relax = Relax(
        atoms=atoms,
        calc=EMT,
        optimizer_factory=lambda atoms: BFGS(atoms),
        symprec=symprec,
        comm=world,
        logfile=logfile,
    )

    relax.run(fmax=fmax, smax=smax)
    txt = logfile.read_text()
    print(txt)
    niter = int(
        [line for line in txt.splitlines() if line.strip()][-1].split()[0]
    )
    assert niter == 7
    assert atoms.get_potential_energy() == pytest.approx(ref_energy)
