""".. _howto_optimization_relaxation:

Simple structure relaxation
===========================
This is a very simple example of a structure relaxation.
"""

from ase.build import molecule
from ase.calculators.emt import EMT
from ase.optimize import BFGS

h2o=molecule('H2O')
h2o.calc=EMT()
optim = BFGS(h2o, trajectory='H2O.traj')
optim.run(fmax=0.05)


