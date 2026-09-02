.. module:: ase.filters

=======
Filters
=======

The Filter class
================

Constraints can also be applied via filters, which acts as a wrapper
around an atoms object. A typical use case will look like this::

   -------       --------       ----------
  |       |     |        |     |          |
  | Atoms |<----| Filter |<----| Dynamics |
  |       |     |        |     |          |
   -------       --------       ----------

and in Python this would be::

  >>> atoms = Atoms(...)
  >>> filter = Filter(atoms, ...)
  >>> dyn = Dynamics(filter, ...)

.. autoclass:: Filter

The UnitCellFilter class
========================

The unit cell filter is for optimizing positions and unit cell
simultaneously.  Note that :class:`ExpCellFilter` will probably
perform better.

.. autoclass:: UnitCellFilter

The StrainFilter class
======================

The strain filter is for optimizing the unit cell while keeping
scaled positions fixed.

.. autoclass:: StrainFilter


The ExpCellFilter class
=======================

The exponential cell filter is an improved :class:`UnitCellFilter`
which is parameter free.

.. autoclass:: ExpCellFilter

The FrechetCellFilter class
===========================

.. autoclass:: FrechetCellFilter
