.. module:: ase.phonons

===================
Phonon calculations
===================

Module for calculating vibrational normal modes for periodic systems using the
so-called small displacement method (see e.g. [Alfe]_). So far, space-group
symmetries are not exploited to reduce the number of atomic displacements that
must be calculated and subsequent symmetrization of the force constants.

A key step in the calculation of phonon modes and energies through small
displacements is the construction of the :math:`\mathbf{q}`-dependent dynamical
matrix from harmonic force constants and phase factors. These phase factors
are determined by the input :math:`\mathbf{q}`-vector and the atom-to-atom
vectors which go from an atom :math:`a_1` in the reference unit cell to an
atom :math:`a_2` in cell :math:`N` in the supercell; however, the due to the
periodicity of the supercell, the shortest vector from :math:`a_1` to atom
:math:`(N, a_2)` is found by checking all the nearest-neighbour periodic
images of :math:`(N, a_2)` and choosing the shortest vector. Furthermore, there
may be multiple images of :math:`(N, a_2)` that yield the shortest vector. In
such cases, it will be beneficial to use the averaged phase factor of all the
shortest atom-to-atom image vectors. For further details on mean minimum image
phases see equation (48) and surrounding text in [Togo]_. In the ASE
:class:`~ase.phonons.Phonons` class, the usage of mean minimum image phases can
be enabled by setting ``use_mean_minimum_images=True`` at class initialization.
This is highly recommended and tends to have much better converged phonon
energies for smaller supercells. The tolerance for detecting mean minimum
images can also be adjusted with the ``mmi_atol`` keyword.

For polar materials the dynamical matrix at the zone center acquires a
non-analytical contribution that accounts for the LO-TO splitting. This
contribution requires additional functionality to evaluate and is not included
in the present implementation. Its implementation in conjunction with the small
displacement method is described in [Wang]_.

Example
=======

Simple example showing how to calculate the phonon dispersion for bulk aluminum
using a 5x5x5 supercell within effective medium theory:

.. literalinclude:: phonons_Al_fcc.py
   :start-after: creates:
   :end-before: literalinclude division line

.. image:: Al_phonon.png

Mode inspection:

.. literalinclude:: phonons_Al_fcc.py
   :start-after: literalinclude division line

.. [Alfe] D. Alfe, PHON: A program to calculate phonons using the small
          displacement method, Comput. Phys. Commun. 180, 2622 (2009)
.. [Togo] A. Togo, *et al.* Implementation strategies in phonopy and phono3py,
          Journal of Physics: Condensed Matter 35.35 (2023): 353001.
.. [Wang] Y. Wang *et al.*, A mixed-space approach to first-principles
          calculations of phonon frequencies for polar materials, J. Phys.:
          Cond. Matter 22, 202201 (2010)


List of all Methods
===================

.. autoclass:: Phonons
   :members:
