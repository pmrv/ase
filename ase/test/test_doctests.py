import doctest
import importlib

import numpy as np
import pytest

module_names = """\
ase.atom
ase.atoms
ase.build.tools
ase.cell
ase.calculators.vasp.vasp
ase.collections.collection
ase.constraints
ase.dft.kpoints
ase.eos
ase.filters
ase.formula
ase.geometry
ase.geometry.analysis
ase.geometry.bravais_type_engine
ase.geometry.dimensionality
ase.geometry.cell
ase.geometry.geometry
ase.geometry.distance
ase.geometry.rdf
ase.geometry.minkowski_reduction
ase.io.ulm
ase.lattice
ase.neighborlist
ase.parallel
ase.phonons
ase.spacegroup.spacegroup
ase.spacegroup.xtal
ase.symbols
ase.io
ase.io.trajectory
ase.io.opls
ase.phasediagram
ase.pourbaix
ase.utils
ase.spectrum
""".split()


@pytest.mark.parametrize('modname', module_names)
def test_doctest(testdir, modname):
    mod = importlib.import_module(modname)
    with np.printoptions(legacy='1.13'):
        doctest.testmod(mod, raise_on_error=True, verbose=True)
