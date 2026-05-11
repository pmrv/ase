""".. _ext_calc_cp2k:

External calculators - CP2K
---------------------------

.. _CP2K: https://www.cp2k.org/

CP2K is a program to perform atomistic and molecular simulations of solid
state, liquid, molecular, and biological systems. It provides a general
framework for different methods such as e.g., density functional theory
(DFT) using a mixed Gaussian and plane waves approach (GPW).

"""

# %%
#
# We perform an example CP2K DFT calculation by first importing the calculator
# for CP2K and creating a bulk silicon example atoms object.

from ase.build import bulk
from ase.calculators.cp2k import CP2K

atoms = bulk('Si')

# %%
#
# Next, we set up a calculator object and specify CP2K's calculation parameters.

calc = CP2K(
    xc='LDA',  # Exchange-correlation functional
    cutoff=400,  # Plane-wave energy cutoff
)

# %%
# and run the calculation:

atoms.calc = calc
energy = atoms.get_potential_energy()
print(energy)
