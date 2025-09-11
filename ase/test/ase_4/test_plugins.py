#!/usr/bin/env python

"""Tests for experimental ASE v4 plugin system."""

import textwrap
from pathlib import Path

import pytest

import ase.test.ase_4.sample_plugins as sample_plugins
from ase import Atoms
from ase._4.plugins import PluginCollection
from ase._4.plugins import plugins as auto_plugins
from ase._4.plugins.plugin import CalculatorPlugin


@pytest.fixture
def sample_calc_plugins():
    """Collection of two calculator plugins"""

    return [sample_plugins.emt_plugin, sample_plugins.lj_plugin]


@pytest.fixture
def sample_mixed_plugins():
    """Collection of two calculator plugins and one ioformat"""
    return [
        sample_plugins.emt_plugin,
        sample_plugins.lj_plugin,
        sample_plugins.extxyz_plugin,
    ]


@pytest.fixture
def two_instances_plugins():
    another_emt_plugin = CalculatorPlugin(
        name='emt',
        metadata={},
        implementation='ase.calculators.emt.EMT',
    )

    return [
        sample_plugins.emt_plugin,
        sample_plugins.lj_plugin,
        another_emt_plugin,
    ]


@pytest.fixture
def sample_atoms() -> Atoms:
    import ase.build

    return ase.build.bulk('Au', cubic=True)


@pytest.fixture(
    scope='module',
    params=[('POSCAR', 'vasp'), ('dftb_in.hsd', 'dftb'), ('tmp.xyz', 'extxyz')],
)
def sample_file_and_format(request) -> tuple[Path, str]:
    filename, format_name = request.param
    path = Path(__file__).parent / f'data/{filename}'
    return path, format_name


@pytest.fixture(scope='module')
def cat_plugin():
    from ase_entry_demo.plugin import Plugin

    class CatPlugin(Plugin): ...

    return CatPlugin(name='Felix', metadata={'fur': 'black'})


def test_build_from_entry_points():
    """Check that plugins were automatically loaded"""
    assert len(auto_plugins) > 0
    assert auto_plugins == auto_plugins
    assert PluginCollection.from_entry_points() == auto_plugins


def test_display(sample_calc_plugins):
    """Check that plugin listing looks correct"""
    assert PluginCollection(sample_calc_plugins).display() == textwrap.dedent(
        """\
        emt                  (ase.test.ase_4.sample_plugins)
        lj                   (ase.test.ase_4.sample_plugins)"""
    )


# def test_calculator_factory(sample_plugins, sample_atoms):
#     from ase_entry_demo.factories import calculator_factory

#     good_collection = PluginCollection(sample_plugins)
#     emt_calculator = calculator_factory("emt", plugins=good_collection)
#     sample_atoms.calc = emt_calculator()
#     sample_atoms.get_potential_energy()


# def test_calculator_factory_warning(two_instances_plugins, sample_atoms):
#     from ase_entry_demo.factories import calculator_factory

#     redundant_collection = PluginCollection(two_instances_plugins)
#     with pytest.warns(UserWarning):
#         first_emt_calculator = calculator_factory(
#             "emt", plugins=redundant_collection
#         )

#     sample_atoms.calc = first_emt_calculator()
#     sample_atoms.get_potential_energy()


def test_cache_invalidation(sample_calc_plugins):
    plugins = PluginCollection(sample_calc_plugins)

    initial_calculators = plugins.calculators
    initial_by_package = plugins.by_package

    # Change the underlying data
    plugins.plugins = frozenset(sample_calc_plugins[:-1])
    new_calculators = plugins.calculators
    new_by_package = plugins.by_package

    assert len(initial_by_package['ase']) != len(new_by_package['ase'])

    assert len(initial_calculators) == 2
    assert len(new_calculators) == 1


# def test_read_function(sample_file_and_format):
#     from ase_entry_demo.factories import read

#     sample_file, file_format = sample_file_and_format

#     atoms = read(sample_file)
#     assert len(atoms) == 4

#     atoms = read(sample_file, format_name=file_format)
#     assert len(atoms) == 4


def test_missing_writer():
    from .sample_plugins import castep_castep_plugin

    assert castep_castep_plugin.can_read
    assert not castep_castep_plugin.can_write


# def _compare_plugins_by_category_with_expected(plugins: PluginCollection,
#                                                expected: str):
#     from io import StringIO

#     from ase_entry_demo.info import print_plugins_by_category

#     buffer = StringIO()
#     print_plugins_by_category(plugins, file=buffer)

#     buffer.seek(0)
#     assert buffer.read() == expected


# def test_print_calculators_by_category(sample_plugins):
#     _compare_plugins_by_category_with_expected(
#         PluginCollection(sample_plugins),
#         """\
# Calculator plugins:
# -------------------
# emt                  (ase_entry_demo.wrappers)
# lj                   (ase_entry_demo.wrappers)

# """)


# def test_print_all_categories(sample_mixed_plugins, cat_plugin):
#     _compare_plugins_by_category_with_expected(
#         PluginCollection(sample_mixed_plugins),
#         """\
# Calculator plugins:
# -------------------
# emt                  (ase_entry_demo.wrappers)
# lj                   (ase_entry_demo.wrappers)

# IO plugins:
# -----------
# extxyz               (ase_entry_demo.wrappers)

# """)

#     _compare_plugins_by_category_with_expected(
#         PluginCollection(sample_mixed_plugins + [cat_plugin]),
#         """\
# Calculator plugins:
# -------------------
# emt                  (ase_entry_demo.wrappers)
# lj                   (ase_entry_demo.wrappers)

# IO plugins:
# -----------
# extxyz               (ase_entry_demo.wrappers)

# CatPlugin:
# ----------
# Felix                (_pytest.fixtures)

# """)
