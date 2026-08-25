.. module:: ase.phonons

===================
Phonon calculations
===================

Module for calculating vibrational normal modes for periodic systems using the
so-called small displacement method (see e.g. [Alfe]_). So far, space-group
symmetries are not exploited to reduce the number of atomic displacements that
must be calculated and subsequent symmetrization of the force constants.

For polar materials the dynamical matrix at the zone center acquires a
non-analytical contribution that accounts for the LO-TO splitting. This
contribution requires additional functionality to evaluate and is not included
in the present implementation. Its implementation in conjunction with the small
displacement method is described in [Wang]_.


List of all Methods
===================

.. autoclass:: Phonons
   :members:


References
===========

.. [Alfe] D. Alfe, PHON: A program to calculate phonons using the small
          displacement method, Comput. Phys. Commun. 180, 2622 (2009)
.. [Wang] Y. Wang *et al.*, A mixed-space approach to first-principles
          calculations of phonon frequencies for polar materials, J. Phys.:
          Cond. Matter 22, 202201 (2010)