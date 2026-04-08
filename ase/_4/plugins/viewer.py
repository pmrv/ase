from __future__ import annotations

from collections.abc import Callable
from functools import cached_property
from typing import (
    TYPE_CHECKING,
)

from typing_extensions import Self

from ase._4.plugins.plugin import Plugin
from ase.utils.plugins import ExternalViewer
from ase.visualize.viewers import AbstractViewer

if TYPE_CHECKING:
    from importlib.metadata import EntryPoint


class ViewerPlugin(Plugin):
    """Container for a Viewer with metadata about where it came from"""

    def __init__(
        self,
        name: str,
        implementation: str | Callable[[], AbstractViewer],
        metadata: dict[str, str] | None = None,
    ) -> None:
        super().__init__(name=name, metadata=metadata)
        self._implementation = implementation

    @cached_property
    def implementation(self) -> AbstractViewer:
        implementation = self._resolve(self._implementation)
        assert isinstance(implementation, AbstractViewer)
        return implementation

    def __call__(self, atoms, *args, **kwargs):
        return self.implementation.view(atoms, *args, **kwargs)


class LegacyViewerPlugin(ViewerPlugin):
    """Wrapper for external viewer plugin using legacy format/entrypoint"""

    def __init__(
        self,
        name: str,
        implementation: str | Callable[[], AbstractViewer],
        metadata: dict[str, str] | None = None,
    ) -> None:
        super().__init__(
            name=name, implementation=implementation, metadata=metadata
        )

    @classmethod
    def from_externalviewer(
        cls,
        name: str,
        ext_viewer: ExternalViewer,
        metadata: dict[str, str] | None = None,
    ) -> Self:
        from ase.visualize.viewers import CLIViewer, PyViewer

        metadata = {} if metadata is None else metadata
        metadata.setdefault('note', 'Imported from legacy ExternalViewer')

        implementation: AbstractViewer
        if ext_viewer.cli:
            implementation = CLIViewer(name, ext_viewer.fmt, ext_viewer.argv)
        else:
            implementation = PyViewer(
                name, ext_viewer.desc, module_name=ext_viewer.module
            )

        return cls(
            name=name,
            implementation=(lambda: implementation),
            metadata=metadata,
        )

    @classmethod
    def from_legacy_entry_point(
        cls,
        entry_point: EntryPoint,
    ) -> Self:
        external_viewer = entry_point.load()
        if not isinstance(external_viewer, ExternalViewer):
            raise TypeError(
                'Wrong type for registering external IO formats '
                f'in format {entry_point.name}, expected '
                'ExternalViewer'
            )
        return cls.from_externalviewer(entry_point.name, external_viewer)
