import doctest
import importlib

import numpy as np
import pytest

import pkgutil
import ase

all_module_names = [module.name for module in pkgutil.walk_packages(
                    ase.__path__, prefix="ase.")]

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

assert set(module_names).issubset(set(all_module_names))

skip_module_names = """
ase.ga.particle_mutations
ase.ga
ase.ga.population
ase.calculators.dmol
ase.ga.standard_comparators
ase.ga.particle_comparator
ase.calculators.kim.kimpy_wrappers
ase.__main__
ase.utils.sphinx_create_png
ase.io.vasp
ase.dft.bandgap
ase.ga.slab_operators
ase.data.g2_1
ase.utils.cube
ase.ga.utilities
ase.calculators.nwchem
ase.io.eon
ase.test.calculator.siesta.test_scripts.CH4.script
ase.calculators.gamess_us
ase.dft.band_structure
ase.calculators.kim
ase.calculators.openmx.reader
ase.cli.run
ase.transport.calculators
ase.ga.multiprocessingrun
ase.dft.bz
ase.ga.parallellocalrun
ase.ga.pbs_queue_run
ase.calculators.elk
ase.ga.soft_mutation
ase.ga.relax_attaches
ase.ga.particle_crossovers
ase.calculators.mopac
ase.calculators.lammpslib
ase.dft.stm
ase.test.calculator.siesta.test_scripts.Na8.script
ase.ga.data
ase.ga.startgenerator
ase.calculators.exciting.exciting
ase.ga.element_crossovers
ase.ga.convergence
ase.calculators.kim.neighborlist
ase.data.isotopes
ase.io.espresso
ase.ga.standardmutations
ase.test.calculator.test_tersoff
ase.io.elk
ase.vibrations.infrared
ase.calculators.orca
ase.ga.offspring_creator
ase.ga.element_mutations
ase.ga.cutandsplicepairing
ase.test.calculator.siesta.test_scripts.H2.script
ase.ga.ofp_comparator
ase.test.calculator.siesta.test_scripts.Si.script
ase.calculators.abinit
""".split()


print(f'Skipping doctest for {len(skip_module_names)} (sub)modules.')
doctest_module_names = set(all_module_names) - set(skip_module_names)


@pytest.mark.parametrize('modname', doctest_module_names)
def test_doctest(testdir, modname):
    if int(np.__version__.split('.')[0]) < 2:
        pytest.skip('Doctests need numpy2+')
    mod = importlib.import_module(modname)
    doctest.testmod(mod, raise_on_error=True, verbose=True)
