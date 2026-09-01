""".. _howto_opls:

Setting up an OPLS force field calculation
==========================================

Modified xyz
============

Suppose, we define the ethanal molecule as extended xyz file 
(``172_ext.xyz``):
"""

# %
#.. literalinclude:: 172_ext.xyz
#
# Then we can read and view the structure using:

from ase.io.opls import OPLSStructure
from ase.visualize import view

# 172_mod.xyz if the file name for the structure above
s = OPLSStructure('172_mod.xyz')
view(s)  # view with real elements
elements = {'CT': 'Si', 'HC': 'H', 'H1': 'He'}
view(s.colored(elements))  # view with fake elements


# %
#Defining the force field
#========================
#
#The definitions of the force field can be stored in an Amber like style 
#(``172_defs.par``):
#
#.. literalinclude:: ../../../ase/test/testdata/172_defs.par
#
#We can write LAMMPS input using the information above:

import runpy

runpy.run_path('write_lammps.py')

# %
# which writes the LAMMPS input files ``lmp_atoms`` defining atoms,  bonds,
# etc., and ``lmp_opls`` defining the corresponding OPLS force field. A
# rudimentary ``lmp_in`` is also written.

