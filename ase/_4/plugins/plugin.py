from __future__ import annotations

import importlib
import inspect
import re
from abc import ABCMeta
from collections.abc import Callable, Iterator, Sequence
from functools import cached_property, singledispatchmethod
from importlib.metadata import EntryPoint, PackageMetadata, metadata
from types import FrameType, ModuleType
from typing import (
    TYPE_CHECKING,
    Any,
    BinaryIO,
    Concatenate,
    Literal,
    TextIO,
    TypeVar,
)

from typing_extensions import Self

from ase.calculators.calculator import BaseCalculator
from ase.io.formats import IOFormat

if TYPE_CHECKING:
    from ase.atoms import Atoms

_I = TypeVar("_I")


class MissingFunction(ValueError):
    """Reader/writer function not found in relevant ase io module"""


class Plugin(metaclass=ABCMeta):
    def __init__(self, *, name: str, metadata: dict[str, str] | None = None
    ) -> None:
        self.name = name
        self.metadata: dict[str, str] = metadata if metadata else {}
        self.module = self._get_module()

    @classmethod
    def _get_module(cls, levels: int = 3) -> ModuleType | None:
        """
        Detect module in which class is instantiated

        This is a good default value for the plugin .module attribute, but can
        be overriden if appropriate.

        The "levels" parameter can also be tweaked to get the expected result
        if more abstraction layers are involved.

        If the plugin is defined in a Python interpreter, return None
        """

        # mypy is convinced that currentframe() can be None.
        # From docs, None is allowed for non-CPython interpreters. Pypy seems
        # to also work fine, so let's just raise an error if it happens.
        frame = inspect.currentframe()
        assert isinstance(frame, FrameType)

        for _ in range(levels):
            frame = cls._f_back(frame)

        module_name = frame.f_globals["__name__"]

        if module_name != "__main__":
            return importlib.import_module(module_name)

        return None

    @staticmethod
    def _f_back(frame: FrameType) -> FrameType:
        """Wrap frame.f_back with a guarantee it won't return None"""
        f_back = frame.f_back
        if f_back is None:
            raise ValueError("Could not determine module context")
        return f_back

    def display(self) -> str:
        module_name = (
            self.module.__name__
            if isinstance(self.module, ModuleType)
            else self.module
        )

        return f"{self.name:<20} ({module_name})"

    @cached_property
    def package(self) -> str:
        if self.module:
            return self.module.__name__.split(".")[0]
        return ""

    def package_data(self) -> PackageMetadata | None:
        if not self.package:
            return None
        return metadata(self.package)

    @singledispatchmethod
    @staticmethod
    def _resolve(implementation: str) -> Any:
        modulename, classname = implementation.rsplit(".", maxsplit=1)
        module = importlib.import_module(modulename)
        return getattr(module, classname)

    @_resolve.register(Callable)  # type: ignore[call-overload,misc]
    @staticmethod
    def _(implementation: Callable[[], Any]) -> Any:
        return implementation()


class CalculatorPlugin(Plugin):
    def __init__(
        self,
        *,
        name: str,
        implementation: str | Callable[[], type[BaseCalculator]],
        metadata: dict[str, str] | None = None,
    ) -> None:
        super().__init__(name=name, metadata=metadata)
        self._implementation = implementation

    @cached_property
    def implementation(self) -> type[BaseCalculator]:
        implementation = self._resolve(self._implementation)
        assert isinstance(implementation, type)
        assert issubclass(implementation, BaseCalculator)
        return implementation

    def __call__(self) -> type[BaseCalculator]:
        return self.implementation


class IOFormatPlugin(Plugin):
    def __init__(
        self,
        *,
        name: str,
        description: str,
        code: str,
        reader: str
        | Callable[[], Callable[..., Atoms | Iterator[Atoms]]]
        | None,
        writer: str
        | Callable[
            [], Callable[Concatenate[str | BinaryIO | TextIO, Atoms, ...], None]
        ]
        | None,
        metadata: dict[str, str] | None = None,
        extensions: list[str] | None = None,
        globs: list[str] | None = None,
        magic: list[str] | None = None,
        magic_regex: bytes | None | None = None,
    ):
        super().__init__(name=name, metadata=metadata)

        if not any((reader, writer)):
            raise ValueError("IOFormatPlugin must provide a reader or a writer")

        self.name = name
        self.description = description

        assert len(code) == 2
        assert code[0] in list("+1")
        assert code[1] in list("BFS")
        self.code = code

        self._reader = reader
        self._writer = writer

        self.extensions = extensions if extensions else []
        self.globs = globs if globs else []
        self.magic = magic if magic else []
        self.magic_regex = magic_regex

    @cached_property
    def can_read(self) -> bool:
        """Check if plugin implements a reader

        If this is false, read() will raise an error
        """
        return self._reader is not None

    @cached_property
    def can_write(self) -> bool:
        """Check if plugin implements a writer

        If this is false, write() will raise an error
        """
        return self._writer is not None

    def read(
        self, *args: list[Any], **kwargs: dict[str, Any]
    ) -> Atoms | Iterator[Atoms]:
        if not self.can_read:
            raise ValueError("This plugin does not implement a reader")
        assert self._resolved_reader is not None
        return self._resolved_reader(*args, **kwargs)

    def write(
        self,
        filename: str | BinaryIO | TextIO,
        images: Atoms | Sequence[Atoms],
        *args: list[Any],
        **kwargs: dict[str, Any],
    ) -> None:
        if not self.can_write:
            raise ValueError("This plugin does not implement a writer")
        assert self._resolved_writer is not None
        self._resolved_writer(filename, images, *args, **kwargs)

    @cached_property
    def _resolved_reader(self) -> Callable[..., Atoms | Iterator[Atoms]] | None:
        if self._reader is None:
            return None
        return self._resolve(self._reader)  # type: ignore[no-any-return]

    @cached_property
    def _resolved_writer(
        self,
    ) -> (
        Callable[
            Concatenate[str | BinaryIO | TextIO, Atoms | Sequence[Atoms], ...],
            None,
        ]
        | None
    ):
        if self._writer is None:
            return None
        return self._resolve(self._writer)  # type: ignore[no-any-return]

    def match_name(self, basename: str) -> bool:
        from fnmatch import fnmatch

        return any(fnmatch(basename, pattern) for pattern in self.globs)

    def match_magic(self, data: bytes) -> bool:
        if self.magic_regex:
            assert not self.magic, "Define only one of magic and magic_regex"
            match = re.match(self.magic_regex, data, re.M | re.S)
            return match is not None

        from fnmatch import fnmatchcase

        return any(
            fnmatchcase(data, magic + b"*")  # type: ignore[operator, type-var]
            for magic in self.magic
        )


class LegacyIOFormatPlugin(IOFormatPlugin):
    """Wrapper for old IOFormat class to new plugin system

    Note that __init__ is the same as IOFormatPlugin: this class
    should typically be constructed using the
    .from_legacy_ioformat or .from_legacy_entry_point classmethod.
    """

    @cached_property
    def can_read(self) -> bool:
        """Check if plugin implements a reader

        If this is false, read() will raise an error

        New IOFormatPlugin stores a missing reader as None, but for legacy
        implementations we have to check the module content at this point.
        """
        try:
            self._resolved_reader
        except MissingFunction:
            return False
        return True

    @cached_property
    def can_write(self) -> bool:
        """Check if plugin implements a writer

        If this is false, write() will raise an error
        """
        try:
            self._resolved_writer
        except MissingFunction:
            return False
        return True

    @staticmethod
    def _legacy_function_loader(
        name: str,
        module_name: str,
        prefix: Literal["read_", "write_"],
        error_message: str,
    ) -> Callable[[], Callable[..., Any]]:
        """Get specially-named function from a module, wrapped in Callable

        This is a compatibility tool for working with the legacy IOFormat

        """

        def func() -> Callable[..., Any]:
            formatname = name.replace("-", "_")
            module = importlib.import_module(module_name)
            legacy_function = getattr(module, prefix + formatname, None)
            if legacy_function is None:
                raise MissingFunction(error_message)
            return legacy_function  # type: ignore[no-any-return]

        return func

    @classmethod
    def from_legacy_io_format(
        cls,
        io_format: IOFormat,
        metadata: dict[str, str] | None = None,
    ) -> Self:
        metadata = metadata if metadata else {}

        reader = cls._legacy_function_loader(
            io_format.name,
            io_format.module_name,
            "read_",
            f"Can't read from {io_format.name}-format",
        )
        writer = cls._legacy_function_loader(
            io_format.name,
            io_format.module_name,
            "write_",
            f"Can't write to {io_format.name}-format",
        )

        plugin = cls(
            name=io_format.name,
            description=io_format.description,
            code=io_format.code,
            reader=reader,
            writer=writer,
            metadata={"note": "Imported from legacy IOFormat"} | metadata,
            extensions=io_format.extensions,
            globs=io_format.globs,
            magic=io_format.magic,
            magic_regex=io_format.magic_regex,
        )

        plugin.module = cls._get_module(levels=2)
        return plugin

    @classmethod
    def from_legacy_entry_point(
        cls,
        entry_point: EntryPoint,
    ) -> Self:
        fmt = entry_point.load()

        reader = cls._legacy_function_loader(
            entry_point.name,
            entry_point.module,
            "read_",
            f"Can't read from {entry_point.name}-format",
        )

        writer = cls._legacy_function_loader(
            entry_point.name,
            entry_point.module,
            "write_",
            f"Can't write to {entry_point.name}-format",
        )

        plugin = cls(
            name=entry_point.name,
            description=fmt.desc,
            code=fmt.code,
            reader=reader,
            writer=writer,
            metadata={"note": "Imported from legacy ExternalIOFormat"},
            extensions=fmt.ext,
            globs=fmt.glob,
            magic=fmt.magic,
            magic_regex=fmt.magic_regex,
        )

        plugin.module = importlib.import_module(fmt.module)
        return plugin
