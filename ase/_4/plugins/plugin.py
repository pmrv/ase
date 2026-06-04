from __future__ import annotations

import importlib
import inspect
from abc import ABCMeta
from collections.abc import Callable
from functools import cached_property, singledispatchmethod
from importlib.metadata import metadata
from types import FrameType, ModuleType
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from ase.calculators.calculator import BaseCalculator

if TYPE_CHECKING:
    from importlib.metadata import PackageMetadata


_I = TypeVar('_I')


class MissingFunction(ValueError):
    """Reader/writer function not found in relevant ase io module"""


class Plugin(metaclass=ABCMeta):
    def __init__(
        self, *, name: str, metadata: dict[str, str] | None = None
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

        module_name = frame.f_globals['__name__']

        if module_name != '__main__':
            return importlib.import_module(module_name)

        return None

    @staticmethod
    def _f_back(frame: FrameType) -> FrameType:
        """Wrap frame.f_back with a guarantee it won't return None"""
        f_back = frame.f_back
        if f_back is None:
            raise ValueError('Could not determine module context')
        return f_back

    def display(self) -> str:
        module_name = (
            self.module.__name__
            if isinstance(self.module, ModuleType)
            else self.module
        )
        return f'{self.name:<20} ({module_name} {self.version})'

    @cached_property
    def package(self) -> str:
        if self.module:
            return self.module.__name__.split('.')[0]
        return ''

    @cached_property
    def package_data(self) -> PackageMetadata | None:
        if not self.package:
            return None
        return metadata(self.package)

    @property
    def version(self) -> str:
        return self.package_data.get('Version', '')

    @singledispatchmethod
    @staticmethod
    def _resolve(implementation: str) -> Any:
        modulename, classname = implementation.rsplit('.', maxsplit=1)
        module = importlib.import_module(modulename)
        return getattr(module, classname)

    @_resolve.register(Callable)  # type: ignore[call-overload,misc]
    @staticmethod
    def _(implementation: Callable[[], Any]) -> Any:
        return implementation()


class CalculatorPlugin(Plugin):
    """Container for a Calculator with metadata about where it came from"""

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
