# fmt: off

# Note:
# Try to avoid module level import statements here to reduce
# import time during CLI execution
from __future__ import annotations

from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from ase._4.plugins.plugin import IOFormatPlugin


class CLICommand:
    """Print information about files or system.

    Without arguments, show information about ASE installation
    and library versions of dependencies.
    """

    @staticmethod
    def add_arguments(parser):
        parser.add_argument('--files', nargs='*', metavar='PATH',
                            help='Print information about specified files.')
        parser.add_argument('-v', '--verbose', action='store_true',
                            help='Show additional information about files.')
        parser.add_argument('--formats', action='store_true',
                            help='List file formats known to ASE.')
        parser.add_argument('--calculators', nargs='*', metavar='NAME',
                            help='List all or specified calculators known to '
                            'ASE and their configuration.')

    @staticmethod
    def run(args):
        if args.calculators is not None:
            from ase.codes import codes, list_codes
            if args.calculators:
                names = args.calculators
            else:
                names = [*codes]
            list_codes(names)
            return

        if args.files:
            print_file_info(args)
            return

        print_info()
        if args.formats:
            print()
            print_formats()


def print_file_info(args):
    from ase.io.bundletrajectory import print_bundletrajectory_info
    from ase.io.formats import UnknownFileTypeError, filetype, ioformats
    from ase.io.ulm import print_ulm_info
    n = max(len(filename) for filename in args.files) + 2
    nfiles_not_found = 0
    for filename in args.files:
        try:
            format = filetype(filename)
        except FileNotFoundError:
            format = '?'
            description = 'No such file'
            nfiles_not_found += 1
        except UnknownFileTypeError:
            format = '?'
            description = '?'
        else:
            if format in ioformats:
                description = ioformats[format].description
            else:
                description = '?'

        print('{:{}}{} ({})'.format(filename + ':', n,
                                    description, format))
        if args.verbose:
            if format == 'traj':
                print_ulm_info(filename)
            elif format == 'bundletrajectory':
                print_bundletrajectory_info(filename)

    raise SystemExit(nfiles_not_found)


def print_info():
    import platform
    import sys

    from ase.dependencies import all_dependencies

    versions = [('platform', platform.platform()),
                ('python-' + sys.version.split()[0], sys.executable)]

    for name, path in versions + all_dependencies():
        print(f'{name:24} {path}')


class IOFormatInfo:
    """Provide methods for read-only info display of IOFormatPlugin"""
    def __init__(self, io_plugin: IOFormatPlugin):
        self._fmt = io_plugin

    def get_name(self) -> str:
        return self._fmt.name

    def get_description(self) -> str:
        return self._fmt.description

    def rw_modes(self) -> Literal['r', 'w', 'rw']:
        return (f'{"r" if self._fmt.can_read else ""}'
                f'{"w" if self._fmt.can_write else ""}')

    def single_or_multi(self) -> Literal['single', 'multi']:
        return 'single' if self._fmt.code[0] == '1' else 'multi'

    def is_binary(self) -> bool:
        return self._fmt.code[1] == 'B'

    def encoding(self) -> str | None:
        return self._fmt.encoding

    def __str__(self) -> str:
        rw_info = [self.rw_modes(), self.single_or_multi()]

        if self.is_binary():
            rw_info.append('binary')
        if (encoding := self.encoding()) is not None:
            rw_info.append(encoding)

        info = ['/'.join(rw_info)]

        if self._fmt.extensions:
            info.append('ext={}'.format('|'.join(self._fmt.extensions)))
        if self._fmt.globs:
            info.append('glob={}'.format('|'.join(self._fmt.globs)))

        return ('  {} [{}]: {}'.format(self.get_name(),
                                       ', '.join(info),
                                       self.get_description()))


def print_formats():
    from operator import attrgetter

    from ase._4.plugins import plugins

    print('Supported formats:')
    for fmt in sorted(plugins.io_formats, key=attrgetter("name")):
        print(IOFormatInfo(fmt))
