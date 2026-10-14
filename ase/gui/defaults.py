"""This is a module to handle generic ASE (gui) defaults ...

... from a ~/.ase/gui.py configuration file, if it exists. It is imported when
opening ASE-GUI and can then be modified at runtime, if necessary. syntax for
each entry:

gui_default_settings['key'] = value
"""

import runpy

gui_default_settings = {
    'gui_graphs_string': 'i, e - E[-1]',  # default for the graph command
    'gui_foreground_color': '#000000',
    'gui_background_color': '#ffffff',
    'covalent_radii': None,
    'radii_scale': 0.89,
    'force_vector_scale': 1.0,
    'velocity_vector_scale': 1.0,
    'magmom_vector_scale': 1.0,
    'show_unit_cell': True,
    'show_axes': True,
    'show_bonds': False,
    # Performance options for large systems.  Both are no-ops for small
    # structures; see View._draw_indices().
    # Draw fewer objects while dragging/zooming:
    'interactive_level_of_detail': True,
    'occlusion_culling': True,  # skip atoms fully obscured by nearer atoms
    'shift_cell': False,
    'swap_mouse': False,
    'movie_rate': 'auto',  # can set to float
    'movie_skip': 'auto',  # can set to int
    'movie_rock': False,
}


def read_defaults():
    import os

    # should look for .config/ase/gui.py
    # if 'XDG_CONFIG_HOME' in os.environ:
    #    name = os.environ['XDG_CONFIG_HOME'] + '/ase/gui.py'
    name = os.path.expanduser('~/.ase/gui.py')
    config = gui_default_settings
    if os.path.exists(name):
        runpy.run_path(
            name, init_globals={'gui_default_settings': gui_default_settings}
        )
    return config
