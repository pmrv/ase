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
ase.optimize.basin
ase.optimize.bfgs
ase.optimize.bfgslinesearch
ase.optimize.cellawarebfgs
ase.optimize.climbfixinternals
ase.optimize.fire
ase.optimize.fire2
ase.optimize.gpmin.gpmin
ase.optimize.lbfgs
ase.optimize.mdmin
ase.optimize.minimahopping
ase.optimize.ode
ase.optimize.oldqn
ase.optimize.optimize
ase.optimize.rfo
ase.optimize.sciopt
ase.parallel
ase.phonons
ase.spacegroup.spacegroup
ase.spacegroup.xtal
ase.symbols
ase.vibrations
ase.vibrations.albrecht
ase.vibrations.data
ase.vibrations.franck_condon
ase.vibrations.pickle2json
ase.vibrations.placzek
ase.vibrations.raman
ase.vibrations.resonant_raman
ase.vibrations.vibrations
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
    if int(np.__version__.split('.')[0]) < 2:
        pytest.skip('Doctests need numpy2+')
    mod = importlib.import_module(modname)
    doctest.testmod(mod, raise_on_error=True, verbose=True)
