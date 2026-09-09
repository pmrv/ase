"""Tests for `NEBTools`."""

import numpy as np
import pytest

from ase import Atoms
from ase.calculators.emt import EMT
from ase.mep.neb import _guess_nimages


@pytest.fixture
def images() -> list[Atoms]:
    symbols = 7 * ['Cu']
    cell = [
        [0.000, 1.805, 1.805],
        [1.805, 0.000, 1.805],
        [1.805, 1.805, 0.000],
    ]
    images = []
    for pos in np.linspace(0.0, 0.5, 6):
        scaled_positions = [
            [0.0, 0.0, pos],
            [0.0, 0.5, 0.0],
            [0.0, 0.5, 0.5],
            [0.5, 0.0, 0.0],
            [0.5, 0.0, 0.5],
            [0.5, 0.5, 0.0],
            [0.5, 0.5, 0.5],
        ]
        atoms = Atoms(
            symbols,
            scaled_positions=scaled_positions,
            cell=cell,
            pbc=True,
        )
        images.append(atoms)
    return images


@pytest.mark.parametrize('repetition', [1, 2])
def test_guess_nimages(images: list[Atoms], repetition: int) -> None:
    """Test if `_guess_nimages` return the expected values.

    This tests a symmetric path with 1 or 2 bands in the images.
    """
    number_of_images = len(images)

    images_extended = []
    for _ in range(repetition):
        for atoms_ref in images:
            atoms = atoms_ref.copy()
            atoms.calc = EMT()
            atoms.get_potential_energy()
            images_extended.append(atoms)

    assert _guess_nimages(images_extended) == number_of_images
