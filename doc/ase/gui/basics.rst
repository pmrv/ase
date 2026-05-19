===================================
GUI basics and command line options
===================================

ASE has a built-in graphical user interface (GUI) which can be invoked from
a terminal with the :command:`ase gui` subcommand and which can read all
the same file formats that the ASE's :func:`~ase.io.read` function
understands:

::

  $ ase gui N2Fe110-path.traj

Type :command:`ase gui -h` for a description of all command line options.

Alternatively, the GUI can be launched from a Python script or an
interactive session by using :func:`ase.visualize.view`. For example, to
view an Atoms object in the GUI *via* Python, do:

>>> from ase.visualize import view
>>> atoms = ...
>>> view(atoms)

.. or

.. >>> view(atoms, repeat=(3, 3, 2))

The methods above open and modify a copy of the Atoms object which can
then be saved to a file. In order to make direct changes to the atoms that
are open in a Python session, use:

>>> atoms.edit()


Selecting a part of a trajectory
................................

When opening files that contain multiple atomic structures, a subset of
the configurations can be selected using Python-like indexing
separated with the @ character, i.e.
:file:`filename@{start}:{stop}:{step}`::

  $ ase gui x.traj@0:10:1  # first 10 images
  $ ase gui x.traj@0:10    # first 10 images
  $ ase gui x.traj@:10     # first 10 images
  $ ase gui x.traj@-10:    # last 10 images
  $ ase gui x.traj@0       # first image
  $ ase gui x.traj@-1      # last image
  $ ase gui x.traj@::2     # every second image

To simultaneously select the same range from many files, use the ``-n``
or ``--image-number`` option::

  $ ase gui -n -1 *.traj   # last image from all .traj files
  $ ase gui -n 0 *.traj    # first image from all .traj files


Basic controls
--------------

Analyzing a system with ASE's GUI is straightforward. The primary (left)
mouse button is used to select/unselect atoms and several atoms can be
selected by holding down the :kbd:`ctrl` modifier key. Clicking and
dragging with the secondary mouse button manipulates the view, rotating by
default or panning around when the :kbd:`shift` modifier is held. Scrolling
with the mouse wheel or touchpad zooms the view in and out. The
:ref:`gui-view` menu contains additional options for efficient view
manipulation.

Depending on how many atoms are selected, the :ref:`ase-gui` automatically
displays certain information in the status bar on the bottom left of the
window:

================================= ======================================
Selection                         Display
================================= ======================================
single atom                       position (x,y,z) and chemical symbol
                                  of the atom
two atoms                         interatomic distance and chemical
                                  symbols
three atoms                       internal angles between the atoms and
                                  chemical symbols
four atoms                        dihedral angle, i.e. the angle between
                                  bonds 1-2 and 3-4, and chemical
                                  symbols
more than four atoms              chemical composition (formula) of
                                  selection
================================= ======================================

Explore the :ref:`gui-edit` menu to find ways to manipulate the selected
atoms as well as their corresponding keyboard shortcuts.


Plotting data from the command line
-----------------------------------
It is possible to make plots using the data in trajectory files directly
from the command line. For example, to plot the energy relative to the
energy of the first image as a function of the distance between
atoms 0 and 5::

  $ ase gui -g "d(0,5),e-E[0]" x.traj
  $ ase gui -t -g "d(0,5),e-E[0]" x.traj > x.dat  # No GUI, write data to stdout

For instructions on creating valid graphing strings, refer to
:ref:`gui-tools graphs`.


.. _gui configuration:

Configuring the GUI
-------------------

Certain defaults for the GUI can be set using a file ``~/.ase/gui.py``.
If the file exists, it is executed after initializing the variables and
colors normally used in ASE.

For example, one can change the default graphs that are plotted, and the
default radii for displaying specific atoms. The following will change the
default graph in the GUI to display the energy evolution and the maximal
force and also display Cu atoms (Z=29) with a radius of 1.6 Angstrom. The
``covalent_radii`` setting also accepts key-value pairs in the form of a
dictionary, and atoms can be referred to using atomic symbols.

::

  gui_default_settings['gui_graphs_string'] = "i, e - min(E), fmax"
  gui_default_settings['covalent_radii'] = [[29,1.6]]  # or {29: 1.6}

To see a list of all settings that can be changed, along with their
default values, do:

::

  from ase.gui.defaults import gui_default_settings
  print(gui_default_settings)


.. _high contrast:

High contrast settings
^^^^^^^^^^^^^^^^^^^^^^

It is possible to change the foreground and background colors used to draw the
atoms, for instance to draw white graphics on a black background. This can be
done in ``~/.ase/gui.py``:

::

  gui_default_settings['gui_foreground_color'] = '#ffffff' #white
  gui_default_settings['gui_background_color'] = '#000000' #black

The color scheme of the windows themselves (i.e. menus, buttons
and text etc.) can be changed by choosing a different desktop theme. In
Ubuntu it is possible to get white on a dark background by selecting the
theme HighContrastInverse under Appearances in the system settings dialog.

To change the color scheme of graphs, configure the default behaviour of
Matplotlib in a similar way by using a file ``~/.matplotlib/matplotlibrc``.
For example:

::

  patch.edgecolor  : white
  text.color       : white
  axes.facecolor   : black
  axes.edgecolor   : white
  axes.labelcolor  : white
  axes.color_cycle : b, g, r, c, m, y, w
  xtick.color      : white
  ytick.color      : white
  grid.color       : white
  figure.facecolor : 0.1
  figure.edgecolor : black


.. _polling:

Polling the GUI
---------------

Use :meth:`ase.gui.gui.GUI.repeat_poll` to interact programmatically
with the GUI, for example to monitor an ongoing calculation
and update the display on the fly.

.. automethod:: ase.gui.gui.GUI.repeat_poll
