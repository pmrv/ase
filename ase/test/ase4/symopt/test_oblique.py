import numpy as np
from ase import Atoms
from ase._4.symopt.relax import SymmetryAdaptedAtoms


def test_oblique():
    cell = np.array(
        [
            6.871958264638166,
            0.0,
            0.0,
            -3.435979132319082,
            6.185040383035336,
            0.0,
            0.0,
            0.0,
            19.74192264375121,
        ]
    ).reshape(3, 3)

    positions = np.array(
        [
            5.569939550493696,
            0.0,
            8.876861983179055,
            1.3020187141444701,
            0.0,
            10.865060660572155,
            1.3062833784489438,
            2.6379468125103815,
            8.350470399495698,
            3.288959089673552,
            0.0,
            7.5,
            0.0,
            4.609899956639001,
            9.870961321875603,
            4.742262510768027,
            3.547093570524955,
            8.350470399495698,
            2.1296957538701418,
            3.547093570524955,
            11.391452244255511,
            3.5829991749646144,
            0.0,
            12.24192264375121,
            3.4359791323190843,
            1.5751404263963347,
            9.870961321875603,
            -1.306283378448943,
            2.6379468125103815,
            11.391452244255511,
        ]
    ).reshape(-1, 3)

    atoms = Atoms(
        numbers=[52, 52, 35, 52, 41, 35, 35, 52, 41, 35],
        cell=cell,
        positions=positions,
        pbc=[True, True, False],
    )

    assert not atoms.cell[2, :2].any()
    assert not atoms.cell[:2, 2].any()

    # symm = SymmetryAdaptedAtoms.from_atoms_spglib(atoms, symprec=0.1)
    symm = SymmetryAdaptedAtoms.from_atoms(atoms, symprec=0.1, symmorphic=False)
    x = symm.get_x()
    assert all(x == 0)
    symm.set_x(x + 0.1)

    assert not atoms.cell[2, :2].any()
    assert not atoms.cell[:2, 2].any()
