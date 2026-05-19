.. _gui-edit:

====
Edit
====

Undo / Redo
-----------
:kbd:`ctrl+Z` (Undo) / :kbd:`ctrl+shift+Z` (Redo)

Undo or redo changes to atoms that were made in the GUI. The GUI keeps
track of the last 20 points in history. However, some actions such as using
the tools in the :ref:`gui-setup` menu will clear the history for practical
reasons.


Select all
----------

Set all atoms as selected.


Invert selection
----------------

Set all selected atoms as unselected and *vice versa*.


Select constrained atoms
------------------------

Sets all atoms which have the :class:`ase.constraints.FixAtoms` constraint
as selected.


Select immobile atoms
---------------------

Sets all atoms which have not moved between the first and last image (to a
tolerance of :math:`1.0 \times 10^{-10}` Å) as selected.


Cut / Copy / Paste
------------------
:kbd:`ctrl+X` (Cut) / :kbd:`ctrl+C` (Copy) / :kbd:`ctrl+V` (Paste)

Cut, copy, and paste operations on the selected atoms.

When pasting, the atoms are placed with their center of mass at the
selection or at their original coordinates if nothing is selected.


Hide / Show selected atoms
--------------------------

Makes the selected atoms invisible or visible again.


Modify
------
:kbd:`ctrl+Y`

Menu to allow modification of the atomic symbol, an attached tag, or
its magnetic moment.


Add atoms
---------
:kbd:`ctrl+A`

For adding single atoms or pre-existing structures (included with ASE or
imported from a file) to an existing atoms object.


Delete selected atoms
---------------------
:kbd:`backspace`


Edit cell
---------
:kbd:`ctrl+E`

Opens a window for editing the cell and applying periodic boundary
conditions.


Edit atoms
----------
:kbd:`A`

Opens an editor window which allows one to identify the atoms and change
their coordinates and chemical identity directly.


First / Previous / Next / Last image
------------------------------------
:kbd:`home` (First) /
:kbd:`page up` (Previous) /
:kbd:`page down` (Next) /
:kbd:`end` (Last)

Navigate between images in the trajectory which is open. See also
:ref:`gui-tools movie`


Append image copy
-----------------

Make a copy of the current image and place it at the end of the trajectory.
