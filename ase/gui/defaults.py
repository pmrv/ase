"""This is a module to handle generic GUI configuration ...

... from the global ASE configuration in ase.config or an ~/.ase/gui.py
configuration file, for backwards compatibility. The configuration is
imported when opening ASE-GUI and can then be modified at runtime, if
necessary.
"""

import ast
import os
import runpy
import warnings

from ase.config import ASE_CONFIG_FILE, Config, cfg

gui_default_settings = {
    'gui_graphs_string': 'i, e - E[-1]',
    'gui_foreground_color': '#000000',  # hex or named color
    'gui_background_color': '#ffffff',  # hex or named color
    'covalent_radii': None,  # Dictionary of {atomic number/symbol: radius}
    'radii_scale': 0.89,
    'force_vector_scale': 1.0,
    'velocity_vector_scale': 1.0,
    'magmom_vector_scale': 1.0,
    'show_unit_cell': True,
    'show_axes': True,
    'show_bonds': False,
    'shift_cell': False,
    'swap_mouse': False,
    'movie_rate': 'auto',  # float or 'auto'
    'movie_skip': 'auto',  # int or 'auto'
    'movie_rock': False,
}  # end (Marker for a literalinclude in the docs. Please do not remove)


class GUIConfig(Config):
    """For interfacing with the GUI configuration in a backwards and
    hopefully forwards compatible way. Designed to be operated like
    a ConfigParser object.
    """

    def __init__(self, config: Config | None = None):
        super().__init__()
        if config is not None:
            self.parser = config.parser
            self.paths = config.paths

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
        value = self.get(option, fallback)
        if value.lower() == 'auto':
            return 'auto'
        return ast.literal_eval(value)

    def set(self, option, value):
        if not self.parser.has_section('gui'):
            self.parser.add_section('gui')
        self.parser.set('gui', option, str(value))


def read_defaults(
    user_cfg: GUIConfig | Config | dict | None = None,
) -> GUIConfig:
    """Retrieves configuration from ASE configuration files (see ase.config).
    Returns a GUIConfig object from which one can get the settings. If user_cfg
    is specified, parses and adapts the provided configuration instead, ignoring
    the global config.
    """
    old_configfile = os.path.expanduser('~/.ase/gui.py')
    if os.path.exists(old_configfile):
        warnings.warn(
            'Found GUI configuration file gui.py which is deprecated'
            '. Use ' + str(ASE_CONFIG_FILE) + ' instead.',
            FutureWarning,
        )
        runpy.run_path(
            old_configfile,
            init_globals={'gui_default_settings': gui_default_settings},
        )

    if user_cfg is None:
        config = GUIConfig(cfg)
    else:
        if isinstance(user_cfg, dict):
            config = GUIConfig()
            config.parser.read_dict(
                {'gui': {k: str(user_cfg[k]) for k in user_cfg}}
            )
            config.paths.append('dict')
        else:
            config = GUIConfig(user_cfg)

    for k in gui_default_settings:
        if k not in config:
            config.set(k, gui_default_settings[k])

    return config
