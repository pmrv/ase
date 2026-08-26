.. module:: ase.atom

The Atom object
===============

ASE defines a python class called :class:`Atom` to setup and handle atoms
in electronic structure and molecular simulations. From a python
script, atoms can be created like this:

>>> from ase import Atom
>>> a1 = Atom('Si', (0, 0, 0))
>>> a2 = Atom('H', (1.3, 0, 0), mass=2)
>>> a3 = Atom(14, position=(0, 0, 0))  # same as a1

.. autoclass:: Atom


Getting an Atom from an Atoms object
------------------------------------

Indexing an :class:`~ase.Atoms` object returns an :class:`Atom` object
still remembering that it belongs to the collective :class:`~ase.Atoms`:

>>> from ase.build import molecule
>>> atoms = molecule('CH4')
>>> atoms.get_positions()
array([[ 0.      ,  0.      ,  0.      ],
       [ 0.629118,  0.629118,  0.629118],
       [-0.629118, -0.629118,  0.629118],
       [ 0.629118, -0.629118, -0.629118],
       [-0.629118,  0.629118, -0.629118]])
>>> a = atoms[2]
>>> a
Atom('H', [np.float64(-0.629118), np.float64(-0.629118), np.float64(0.629118)], index=2)

Modifying an :class:`Atom` object will also change the :class:`~ase.atoms` object:

>>> a.x = 0
>>> atoms.get_positions()
array([[ 0.      ,  0.      ,  0.      ],
       [ 0.629118,  0.629118,  0.629118],
       [ 0.      , -0.629118,  0.629118],
       [ 0.629118, -0.629118, -0.629118],
       [-0.629118,  0.629118, -0.629118]])


Builing and Atoms object from Atom objects
------------------------------------------

It is also possible to create an :class:`~ase.Atoms` object from an :class:`Atom` object:

>>> from ase.atoms import Atoms
>>> a1 = Atom('H', (0, 0, 0), mass=2)
>>> a2 = Atom('H', (0.74, 0, 0), mass=2)
>>> h2=Atoms([a1,a2])
>>> h2.get_center_of_mass()
array([0.37, 0.  , 0.  ])

.. seealso::

   :mod:`ase`:
     More information about how to use collections of atoms.

   :mod:`ase.calculators`:
     Information about how to calculate forces and energies of atoms.

   :ref:`tips` :
     General tips for using ase.

