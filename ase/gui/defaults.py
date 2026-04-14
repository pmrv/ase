"""This is a module to handle generic GUI configuration ...

... from the global ASE configuration in ase.config or an ~/.ase/gui.py
configuration file, for backwards compatibility. The configuration is
imported when opening ASE-GUI and can then be modified at runtime, if
necessary.
"""
import ast
import os
import runpy

from ase.config import Config

gui_default_settings = {
    'gui_graphs_string': 'i, e - E[-1]',
    'gui_foreground_color': '#000000',  # hex or named color
    'gui_background_color': '#ffffff',  # hex or named color
    'covalent_radii': None,
    'radii_scale': 0.89,
    'force_vector_scale': 1.0,
    'velocity_vector_scale': 1.0,
    'magmom_vector_scale': 1.0,
    'show_unit_cell': True,
    'show_axes': True,
    'show_bonds': False,
    'shift_cell': False,
    'swap_mouse': False,
    'movie_rate': 'auto',  # can set to float
    'movie_skip': 'auto',  # can set to int
    'movie_rock': False,
}


class GUIConfig(Config):
    def _env(self):
        if self.parser.has_section('gui'):
            return self.parser['gui']
        else:
            return self.parser

    def get(self, option, fallback=None):
        return self.parser.get('gui', option, fallback=fallback)

    def getint(self, option, fallback=None):
        return self.parser.getint('gui', option, fallback=fallback)

    def getfloat(self, option, fallback=None):
        return self.parser.getfloat('gui', option, fallback=fallback)

    def getboolean(self, option, fallback=None):
        return self.parser.getboolean('gui', option, fallback=fallback)

    def getliteral(self, option, fallback=None):
        try:
            return ast.literal_eval(self.get(option, fallback))
        except ValueError:
            return self.get(option, fallback=fallback)

    def set(self, option, value):
        self.parser.set('gui', option, value)


def read_defaults():
    """Read ASE configuration files and return an object from which settings
    can be retrieved.
    """

    # should look for .config/ase/gui.py
    # if 'XDG_CONFIG_HOME' in os.environ:
    #    name = os.environ['XDG_CONFIG_HOME'] + '/ase/gui.py'
    old_configfile = os.path.expanduser('~/.ase/gui.py')
    if os.path.exists(old_configfile):
        runpy.run_path(old_configfile, init_globals={'gui_default_settings':
                                           gui_default_settings})

    config = GUIConfig.read(
        defaults={
            'gui': {
                k: str(gui_default_settings[k]) for k in gui_default_settings
            }
        }
    )
    return config
