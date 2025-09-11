from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from ase._4.plugins.plugin import LegacyIOFormatPlugin
from ase.io.formats import ioformats

wrapped_ioformats = {
    LegacyIOFormatPlugin.from_legacy_io_format(ioformat)
    for ioformat in ioformats.values()
}

__ase_plugins__ = wrapped_ioformats
