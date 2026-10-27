.. module:: ase.build

================
Building things
================

Quick links:

* Simple bulk crystals: :func:`~ase.build.bulk`

* Simple molecules: :func:`~ase.build.molecule`

* Special surfaces:

  * fcc: :func:`~ase.build.fcc100`, :func:`~ase.build.fcc110`,
    :func:`~ase.build.fcc111`, :func:`~ase.build.fcc211`,
    :func:`~ase.build.fcc111_root`

  * bcc: :func:`~ase.build.bcc100`, :func:`~ase.build.bcc110`,
    :func:`~ase.build.bcc111`
    * - :func:`~ase.build.bcc111_root`

  * hcp: :func:`~ase.build.hcp0001`, :func:`~ase.build.hcp10m10`,
    :func:`~ase.build.hcp0001_root`

  * diamond: :func:`~ase.build.diamond100`, :func:`~ase.build.diamond111`

* :mol:`MX_2` (2H or 1T): :func:`~ase.build.mx2`

* Other surface tools: :func:`~ase.build.surface`,
  :func:`~ase.build.add_adsorbate`, :func:`~ase.build.add_vacuum`,
  :func:`~ase.build.root_surface`

* 1D: :func:`~ase.build.nanotube`, :func:`~ase.build.graphene_nanoribbon`

* Other tools: :func:`~ase.build.cut`, :func:`~ase.build.stack`,
  :func:`~ase.build.sort`, :func:`~ase.build.minimize_tilt`,
  :func:`~ase.build.niggli_reduce`, :func:`~ase.build.rotate`,
  :func:`~ase.build.minimize_rotation_and_translation`,
  :func:`~ase.build.get_deviation_from_optimal_cell_shape`,
  :func:`~ase.build.find_optimal_cell_shape`,
  :func:`~ase.build.make_supercell`

* Separation: :func:`~ase.build.connected_indices`,
  :func:`~ase.build.connected_atoms`, :func:`~ase.build.separate`,
  :func:`~ase.build.split_bond`

.. toctree::
   :maxdepth: 2

   surface
   tools
   connected

.. seealso::

   * The :mod:`ase.lattice` module.  The module contains functions for
     creating most common crystal structures with arbitrary orientation.
     The user can specify the desired Miller index along the three axes
     of the simulation, and the smallest periodic structure fulfilling
     this specification is created.  Both bulk crystals and surfaces can
     be created.

   * The :mod:`ase.cluster` module.  Useful for creating nanoparticles
     and clusters.

   * The :mod:`ase.spacegroup` module

   * The :mod:`ase.geometry` module



Molecules
=========

The G2-database of common molecules is available:

.. autofunction:: molecule

More complicated molecules may be obtained using the PubChem API integration in
the :func:`~ase.data.pubchem.pubchem_atoms_search` and :func:`~ase.data.pubchem.pubchem_atoms_conformer_search`
functions. You may search based on common name, chemical identification number 
(cid), smiles string, or conformer identification number.

.. _bulk-crystal-section:

Common bulk crystals
====================

.. autofunction:: bulk

|a1| |a2| |a3|

.. |a1| image:: a1.png
.. |a2| image:: a2.png
.. |a3| image:: a3.png


.. _nanotubes-section:

Nanotubes
=========

.. autofunction:: nanotube


|cnt1| |cnt2|

.. |cnt1| image:: cnt1.png
.. |cnt2| image:: cnt2.png


.. _nanoribbons-section:

Graphene nanoribbons
====================

.. autofunction:: graphene_nanoribbon

|gnr1| |gnr2|

.. |gnr1| image:: gnr1.png
.. |gnr2| image:: gnr2.png

ASE contains a number of modules for setting up atomic structures,
mainly molecules, bulk crystals and surfaces.  Some of these modules
have overlapping functionality, but strike a different balance between
flexibility and ease-of-use.

.. _attaching-section:

Attaching structures
====================

.. autofunction:: ase.build.attach.attach
.. autofunction:: ase.build.attach.attach_randomly
.. autofunction:: ase.build.attach.attach_randomly_and_broadcast
