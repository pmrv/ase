# fmt: off

from dataclasses import dataclass

# Note: There could be more than one "calculator" for any given code;
# for example Espresso can work both as GenericFileIOCalculator and
# SocketIOCalculator, or as part of some DFTD3 combination.
#
# Also, DFTD3 is one external code but can be invoked alone (as PureDFTD3)
# as well as together with a DFT code (the main DFTD3 calculator).
#
# The current CodeMetadata object only specifies a single calculator class.
# We should be wary of these invisible "one-to-one" restrictions.


@dataclass
class CodeMetadata:
    name: str
    longname: str
    modulename: str
    classname: str
    uses_config: bool = True

    def calculator_class(self):
        from importlib import import_module
        module = import_module(self.modulename)
        cls = getattr(module, self.classname)
        return cls

    @classmethod
    def define_code(cls, name, longname, importpath, uses_config=True):
        modulename, classname = importpath.rsplit('.', 1)
        return cls(
            name, longname, modulename, classname, uses_config=uses_config)

    def _description(self):
        yield f'Name:     {self.longname}'
        yield f'Import:   {self.modulename}.{self.classname}'
        yield f'Type:     {self.calculator_type()}'
        yield from self._config_description()

    def description(self, indent=''):
        return '\n'.join(indent + line for line in self._description())

    def is_legacy_fileio(self):
        from ase.calculators.calculator import FileIOCalculator
        return issubclass(self.calculator_class(), FileIOCalculator)

    def is_generic_fileio(self):
        from ase.calculators.genericfileio import CalculatorTemplate

        # It is nicer to check for the template class, since it has the name,
        # but then calculator_class() should be renamed.
        return issubclass(self.calculator_class(), CalculatorTemplate)

    def is_calculator_oldbase(self):
        from ase.calculators.calculator import Calculator
        return issubclass(self.calculator_class(), Calculator)

    def is_base_calculator(self):
        from ase.calculators.calculator import BaseCalculator
        return issubclass(self.calculator_class(), BaseCalculator)

    def calculator_type(self):
        cls = self.calculator_class()

        if self.is_generic_fileio():
            return 'GenericFileIOCalculator'

        if self.is_legacy_fileio():
            return 'FileIOCalculator (legacy)'

        if self.is_calculator_oldbase():
            return 'Calculator (legacy base class)'

        if self.is_base_calculator():
            return 'Base calculator'

        return f'BAD: Not a proper calculator (superclasses: {cls.__mro__})'

    def profile(self):
        from ase.calculators.calculator import FileIOCalculator
        from ase.calculators.genericfileio import CalculatorTemplate
        from ase.config import cfg
        cls = self.calculator_class()
        if issubclass(cls, CalculatorTemplate):
            return cls().load_profile(cfg)
        elif hasattr(cls, 'fileio_rules'):
            assert issubclass(cls, FileIOCalculator)
            return cls.load_argv_profile(cfg, self.name)
        else:
            raise NotImplementedError('profile() not implemented')

    def _config_description(self):
        from ase.calculators.genericfileio import BadConfiguration
        from ase.config import cfg

        if not self.uses_config:
            return

        yield ''

        parser = cfg.parser
        if self.name not in parser:
            yield f'Not configured: No [{self.name}] section in configuration'
            return

        try:
            profile = self.profile()
        except BadConfiguration as ex:
            yield f'Error in configuration section [{self.name}]'
            yield 'Missing or bad parameters:'
            yield f'  {ex}'
            return
        except NotImplementedError as ex:
            yield f'N/A: {ex}'
            return

        yield f'Configured by section [{self.name}]:'
        configvars = vars(profile)
        for name in sorted(configvars):
            yield f'  {name} = {configvars[name]}'

        return


def register_codes():

    codes = {}

    def reg(name, *args, **kwargs):
        code = CodeMetadata.define_code(name, *args, **kwargs)
        codes[name] = code

    reg('abinit', 'Abinit', 'ase.calculators.abinit.AbinitTemplate')
    reg('ace', 'ACE molecule', 'ase.calculators.acemolecule.ACE')
    reg('acn', 'ACN force field', 'ase.calculators.acn.ACN', uses_config=False)
    reg('aims', 'FHI-Aims', 'ase.calculators.aims.AimsTemplate')
    reg('amber', 'Amber', 'ase.calculators.amber.Amber')
    reg('average', 'AverageCalculator (wrapper)',
        'ase.calculators.mixing.AverageCalculator', uses_config=False)
    reg('castep', 'Castep', 'ase.calculators.castep.Castep')
    reg('checkpoint', 'CheckpointCalculator (wrapper)',
        'ase.calculators.checkpoint.CheckpointCalculator', uses_config=False)
    reg('combine_mm', 'CombineMM (wrapper)',
        'ase.calculators.combine_mm.CombineMM', uses_config=False)
    reg('counterion', 'AtomicCounterIon',
        'ase.calculators.counterions.AtomicCounterIon', uses_config=False)
    reg('cp2k', 'CP2K', 'ase.calculators.cp2k.CP2K')
    reg('crystal', 'CRYSTAL', 'ase.calculators.crystal.CRYSTAL')
    reg('demon', 'deMon', 'ase.calculators.demon.Demon')
    reg('demonnano', 'deMon-nano', 'ase.calculators.demonnano.DemonNano')
    reg('dftb', 'DFTB+', 'ase.calculators.dftb.Dftb')
    reg('dftd3', 'DFT-D3', 'ase.calculators.dftd3.DFTD3')
    # Implementation detail, best not advertised directly
    # reg('dftd3-pure', 'DFT-D3 (pure)', 'ase.calculators.dftd3.PureDFTD3')
    reg('dmol', 'DMol3', 'ase.calculators.dmol.DMol3')
    reg('eam', 'EAM', 'ase.calculators.eam.EAM', uses_config=False)
    reg('eiqmmmm', 'Explicit interaction QMMM (wrapper)',
        'ase.calculators.qmmm.EIQMMM', uses_config=False)
    reg('elk', 'ELK', 'ase.calculators.elk.ELK')
    reg('emt', 'EMT potential', 'ase.calculators.emt.EMT', uses_config=False)
    reg('espresso', 'Quantum Espresso',
        'ase.calculators.espresso.EspressoTemplate')
    reg('exciting', 'Exciting',
        'ase.calculators.exciting.exciting.ExcitingGroundStateTemplate')
    reg('ff', 'FF', 'ase.calculators.ff.ForceField', uses_config=False)
    reg('fd', 'Finite Difference (wrapper)',
        'ase.calculators.fd.FiniteDifferenceCalculator', uses_config=False)
    # fleur <- external nowadays
    reg('forceconstant', 'ForceConstantCalculator',
        'ase.calculators.qmmm.ForceConstantCalculator', uses_config=False)
    reg('force-qmmmm', 'Force-based QM/MM Calculator (wrapper)',
        'ase.calculators.qmmm.ForceQMMM', uses_config=False)
    reg('gamess_us', 'GAMESS-US', 'ase.calculators.gamess_us.GAMESSUS')
    reg('gaussian', 'Gaussian', 'ase.calculators.gaussian.Gaussian')
    reg('gromacs', 'Gromacs', 'ase.calculators.gromacs.Gromacs')
    reg('gulp', 'GULP', 'ase.calculators.gulp.GULP')
    # h2morse.py do we need a specific H2 morse calculator when we have morse??
    reg('harmonic', 'Harmonic potential',
        'ase.calculators.harmonic.HarmonicCalculator', uses_config=False)
    reg('idealgas', 'Ideal gas (dummy)',
        'ase.calculators.idealgas.IdealGas', uses_config=False)
    # XXX cannot import without kimpy installed, fixme:
    # reg('kim', 'OpenKIM', 'ase.calculators.kim.kim.KIM')
    reg('lammpslib', 'Lammps (python library)',
        'ase.calculators.lammpslib.LAMMPSlib')
    reg('lammpsrun', 'Lammps (external)', 'ase.calculators.lammpsrun.LAMMPS')
    reg('linearcombination', 'LinearCombinationCalculator (wrapper)',
        'ase.calculators.mixing.LinearCombinationCalculator',
        uses_config=False)
    reg('lj', 'Lennard–Jones potential', 'ase.calculators.lj.LennardJones',
        uses_config=False)
    reg('logging', 'LoggingCalculator (wrapper)',
        'ase.calculators.loggingcalc.LoggingCalculator', uses_config=False)
    reg('mixed', 'MixedCalculator (wrapper)',
        'ase.calculators.mixing.MixedCalculator', uses_config=False)
    reg('mopac', 'MOPAC', 'ase.calculators.mopac.MOPAC')
    reg('morse', 'Morse potential', 'ase.calculators.morse.MorsePotential',
        uses_config=False)
    reg('nwchem', 'NWChem', 'ase.calculators.nwchem.NWChem')
    reg('octopus', 'Octopus', 'ase.calculators.octopus.OctopusTemplate')
    reg('onetep', 'Onetep', 'ase.calculators.onetep.OnetepTemplate')
    reg('openmx', 'OpenMX', 'ase.calculators.openmx.OpenMX')
    reg('orca', 'ORCA', 'ase.calculators.orca.OrcaTemplate')
    reg('plumed', 'Plumed', 'ase.calculators.plumed.Plumed')
    reg('psi4', 'Psi4', 'ase.calculators.psi4.Psi4')
    reg('python-subprocess', 'PythonSubProcessCalculator',
        'ase.calculators.subprocesscalculator.PythonSubProcessCalculator',
        uses_config=False)
    reg('qchem', 'QChem', 'ase.calculators.qchem.QChem')
    reg('rescaled', 'Rescaled Calculator (wrapper)',
        'ase.calculators.qmmm.RescaledCalculator', uses_config=False)
    reg('siesta', 'SIESTA', 'ase.calculators.siesta.Siesta')
    reg('simple-qmmmm', 'Simple QMMM (wrapper)',
        'ase.calculators.qmmm.SimpleQMMM', uses_config=False)
    reg('singlepoint', 'SinglePoint',
        'ase.calculators.singlepoint.SinglePointCalculator', uses_config=False)
    reg('singlepoint-dft', 'SinglePointDFTCalculator',
        'ase.calculators.singlepoint.SinglePointDFTCalculator',
        uses_config=False)
    reg('socketio', 'SocketIOCalculator (wrapper)',
        'ase.calculators.socketio.SocketIOCalculator', uses_config=False)
    reg('spring', 'Spring Calculator',
        'ase.calculators.harmonic.SpringCalculator', uses_config=False)
    reg('sum', 'jsumCalculator (wrapper)',
        'ase.calculators.mixing.SumCalculator', uses_config=False)
    reg('tersoff', 'Tersoff potential',
        'ase.calculators.tersoff.Tersoff', uses_config=False)
    # internal: test.py
    reg('tip3p', 'TIP3P', 'ase.calculators.tip3p.TIP3P', uses_config=False)
    reg('tip4p', 'TIP4P', 'ase.calculators.tip4p.TIP4P', uses_config=False)
    reg('turbomole', 'Turbomole', 'ase.calculators.turbomole.Turbomole')
    reg('vasp', 'VASP', 'ase.calculators.vasp.Vasp')
    # internal: vdwcorrection  # This only really works with GPAW, could move?
    return codes


codes = register_codes()


def list_codes(names):
    from ase.config import cfg
    cfg.print_header()
    print()

    for name in names:
        code = codes[name]
        print(code.name)
        try:
            print(code.description(indent='  '))
        except Exception as ex:
            print(f'Bad configuration of {name}: {ex!r}')
        print()


if __name__ == '__main__':
    import sys
    names = sys.argv[1:]
    if not names:
        names = [*codes]
    list_codes(names)
