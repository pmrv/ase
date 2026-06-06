from __future__ import annotations

from ase._4.plugins.io import LegacyIOFormatPlugin
from ase._4.plugins.viewer import ViewerPlugin
from ase.io.formats import ioformats
from ase.visualize.viewers import CLI_VIEWERS, PY_VIEWERS

wrapped_ioformats = {
    LegacyIOFormatPlugin.from_legacy_io_format(ioformat)
    for ioformat in ioformats.values()
}

wrapped_cli_viewers = {
    ViewerPlugin(
        name=key,
        citation='imported from ase.visualize.viewers.CLI_VIEWERS',
        implementation=(lambda: value),
    )
    for key, value in CLI_VIEWERS.items()
}

wrapped_py_viewers = {
    ViewerPlugin(
        name=key,
        citation='imported from ase.visualize.viewers.CLI_VIEWERS',
        implementation=(lambda: value),
    )
    for key, value in PY_VIEWERS.items()
}

__ase_plugins__ = wrapped_ioformats | wrapped_cli_viewers | wrapped_py_viewers
