""".. _phonons:

===================================================
Phonon calculations with small displacement method
===================================================

Simple example showing how to calculate the phonon dispersion for bulk aluminum
using a 7x7x7 supercell within effective medium theory:
"""

# %%
import matplotlib.pyplot as plt
import numpy as np

from ase.build import bulk
from ase.calculators.emt import EMT
from ase.phonons import Phonons

# %%
# Setup Al crystal
atoms = bulk('Al', 'fcc', a=4.05)

# %%
# Setup phonon calculation with EMT calculator
N = 7
ph = Phonons(atoms, EMT(), supercell=(N, N, N), delta=0.05)
ph.run()

# %%
# Read forces and assemble the dynamical matrix
ph.read(acoustic=True)
ph.clean()

# %%
# Set and plot phonon band-structure along specific path
path = atoms.cell.bandpath('GXULGK', npoints=100)
bs = ph.get_band_structure(path)

# Get phonon dos
dos = ph.get_dos(kpts=(20, 20, 20)).sample_grid(npts=100, width=1e-3)
fig = plt.figure(figsize=(7, 4))
ax = fig.add_axes([0.12, 0.07, 0.67, 0.85])


# Plot phonon band-structure and dos
emax = 0.035
bs.plot(ax=ax, emin=0.0, emax=emax)

dosax = fig.add_axes([0.8, 0.07, 0.17, 0.85])
dosax.fill_between(
    dos.get_weights(),
    dos.get_energies(),
    y2=0,
    color='grey',
    edgecolor='k',
    lw=1,
)

dosax.set_ylim(0, emax)
dosax.set_yticks([])
dosax.set_xticks([])
dosax.set_xlabel('DOS', fontsize=18)
plt.show()

# fig.savefig('Al_phonon.png')

# %%
from ase.io.trajectory import Trajectory  # noqa
from ase.io import write  # noqa

# Write modes for specific q-vector to trajectory files:
L = np.array(path.special_points['L'])
ph.write_modes(
    L / 2.0,
    branches=[2],
    repeat=(8, 8, 8),
    kT=3e-4,
    center=True,
)

# Generate gif animation:
# XXX Temporarily disabled due to matplotlib writer compatibility issue.
# with Trajectory('phonon.mode.2.traj', 'r') as traj:
#     write('Al_mode.gif', traj, interval=50,
#           rotation='-36x,26.5y,-25z')
