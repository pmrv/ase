import doctest
import importlib
import pkgutil

import numpy as np
import pytest

import ase

all_module_names = [
    module.name for module in pkgutil.walk_packages(ase.__path__, prefix='ase.')
]

skip_module_names = """
ase.__main__
ase.calculators.abinit
ase.calculators.dmol
ase.calculators.elk
ase.calculators.exciting.exciting
ase.calculators.gamess_us
ase.calculators.kim
ase.calculators.kim.kimpy_wrappers
ase.calculators.kim.neighborlist
ase.calculators.lammpslib
ase.calculators.mopac
ase.calculators.nwchem
ase.calculators.openmx.reader
ase.calculators.orca
ase.cli.run
ase.data.g2_1
ase.data.isotopes
ase.dft.band_structure
ase.dft.bandgap
ase.dft.bz
ase.dft.stm
ase.ga
ase.ga.convergence
ase.ga.cutandsplicepairing
ase.ga.data
ase.ga.element_crossovers
ase.ga.element_mutations
ase.ga.multiprocessingrun
ase.ga.offspring_creator
ase.ga.ofp_comparator
ase.ga.particle_comparator
ase.ga.particle_crossovers
ase.ga.particle_mutations
ase.ga.parallellocalrun
ase.ga.pbs_queue_run
ase.ga.population
ase.ga.relax_attaches
ase.ga.slab_operators
ase.ga.soft_mutation
ase.ga.standard_comparators
ase.ga.standardmutations
ase.ga.startgenerator
ase.ga.utilities
ase.io.elk
ase.io.eon
ase.io.espresso
ase.io.vasp
ase.transport.calculators
ase.utils.cube
ase.utils.sphinx_create_png
ase.utils.structure_comparator
ase.vibrations.infrared
""".split()


print(f'Skipping doctest for {len(skip_module_names)} (sub)modules.')
module_names = set(all_module_names) - set(skip_module_names)

# remove some modules like ase.test, ase.gui
rem_modules = [
    modname
    for name in ['ase.test', 'ase.gui']
    for modname in module_names
    if name in modname
]
module_names -= set(rem_modules)

# sort names
sorted_module_names = sorted(module_names)


@pytest.mark.parametrize('modname', sorted_module_names)
def test_doctest(testdir, modname):
    if int(np.__version__.split('.')[0]) < 2:
        pytest.skip('Doctests need numpy2+')
    mod = importlib.import_module(modname)
    doctest.testmod(mod, raise_on_error=True, verbose=True)
