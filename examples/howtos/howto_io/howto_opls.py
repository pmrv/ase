""".. _howto_opls_setup:

Setting up an OPLS force field calculation
==========================================


Suppose, we define the ethanal molecule as extended xyz file
(``172_ext.xyz``):
"""

# %%
# .. literalinclude:: .../examples/howtos/howto_io/172_ext.xyz
#
# Then we can read and view the structure using:

from ase.io.opls import OPLSStructure
from ase.visualize import view

s = OPLSStructure('172_ext.xyz')
view(s)  # view with real elements
elements = {'CT': 'Si', 'HC': 'H', 'H1': 'He'}
view(s.colored(elements))  # view with fake elements


# %%
# Defining the force field
# ------------------------
#
# The definitions of the force field can be stored in an Amber like style
# (``172_defs.par``):
#
# .. literalinclude:: 172_defs.par
#
# We can write LAMMPS input using the information above:

from ase.io.opls import OPLSff, OPLSStructure

s = OPLSStructure('.../examples/howtos/howto_io/172_ext.xyz')
with open('172_defs.par') as fd:
    opls = OPLSff(fd)
opls.write_lammps(s, prefix='lmp')

# %%
# which writes the LAMMPS input files ``lmp_atoms`` defining atoms,  bonds,
# etc., and ``lmp_opls`` defining the corresponding OPLS force field. A
# rudimentary ``lmp_in`` is also written.
