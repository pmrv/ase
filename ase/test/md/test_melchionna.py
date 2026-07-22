import numpy as np
import pytest

from ase import Atoms
from ase.md.melchionna import MelchionnaNPT
from ase.units import fs


@pytest.mark.parametrize(
    'strain_rate',
    [np.array([[1.0, 1.0, 1.0],
               [0.0, 1.0, 1.0],
               [0.0, 0.0, 1.0]]),
    np.array([[1.0, 0.0, 0.0],
              [1.0, 1.0, 0.0],
              [1.0, 1.0, 1.0]])]
     )
def test_melchionna_npt_set_strain_rate(strain_rate):
    atoms = Atoms('H', cell=10 * np.eye(3), pbc=True)
    dynamics = MelchionnaNPT(atoms,
                             timestep=1.0 * fs,
                             temperature_K=300)

    dynamics.set_strain_rate(strain_rate)

    np.testing.assert_array_equal(
        dynamics.get_strain_rate(),
        strain_rate,
    )
