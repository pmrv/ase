""".. _howto_optimization_relaxation:

Simple structure relaxation
===========================
"""
# %%
# This is a very simple example of a structure relaxation.

from ase.build import molecule
from ase.calculators.emt import EMT
from ase.optimize import BFGS

atoms = molecule('H2O')
atoms.calc = EMT()
opt = BFGS(atoms, trajectory='H2O.traj')
opt.run(fmax=0.05)
