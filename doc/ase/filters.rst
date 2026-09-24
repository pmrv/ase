.. module:: ase.filters

=======
Filters
=======

Filters act as a wrapper around an :class:`~ase.Atoms` object in order to modify
its degrees of freedom during structure optimization.
A typical use case will look like this::

   -------       --------       ----------
  |       |     |        |     |          |
  | Atoms |<----| Filter |<----| Dynamics |
  |       |     |        |     |          |
   -------       --------       ----------

and in Python this would be::

  >>> atoms = Atoms(...)
  >>> filter = Filter(atoms, ...)
  >>> dyn = Dynamics(filter, ...)

The following filters are available:

.. list-table::
    :widths: 25 75

    * - :class:`Filter`
      - fix positions of specified atoms
    * - :class:`StrainFilter`
      - relax cell shape with fixing scaled positions of atoms
    * - :class:`UnitCellFilter`
      - relax both atomic positions and cell shape
    * - :class:`ExpCellFilter`
      - relax both atomic positions and cell shape
    * - :class:`FrechetCellFilter`
      - relax both atomic positions and cell shape

.. autoclass:: Filter

.. autoclass:: StrainFilter

.. autoclass:: UnitCellFilter

.. autoclass:: ExpCellFilter

.. autoclass:: FrechetCellFilter
