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
    config: bool = True

    def calculator_class(self):
        from importlib import import_module
        module = import_module(self.modulename)
        cls = getattr(module, self.classname)
        return cls

    @classmethod
    def define_code(cls, name, longname, importpath, config=True):
        modulename, classname = importpath.rsplit('.', 1)
        return cls(
            name, longname, modulename, classname, config=config)

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

        if not self.config:
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

    def reg(name, *args, config=False):
        code = CodeMetadata.define_code(name, *args, config=config)
        codes[name] = code

    reg('abinit', 'Abinit', 'ase.calculators.abinit.AbinitTemplate',
        config=True)
    reg('ace', 'ACE molecule', 'ase.calculators.acemolecule.ACE', config=True)
    reg('acn', 'ACN force field', 'ase.calculators.acn.ACN')
    reg('aims', 'FHI-Aims', 'ase.calculators.aims.AimsTemplate', config=True)
    reg('amber', 'Amber', 'ase.calculators.amber.Amber', config=True)
    reg('average', 'AverageCalculator (wrapper)',
        'ase.calculators.mixing.AverageCalculator')
    reg('castep', 'Castep', 'ase.calculators.castep.Castep', config=True)
    reg('checkpoint', 'CheckpointCalculator (wrapper)',
        'ase.calculators.checkpoint.CheckpointCalculator')
    reg('combine_mm', 'CombineMM (wrapper)',
        'ase.calculators.combine_mm.CombineMM')
    reg('counterion', 'AtomicCounterIon',
        'ase.calculators.counterions.AtomicCounterIon')
    reg('cp2k', 'CP2K', 'ase.calculators.cp2k.CP2K', config=True)
    reg('crystal', 'CRYSTAL', 'ase.calculators.crystal.CRYSTAL', config=True)
    reg('demon', 'deMon', 'ase.calculators.demon.Demon', config=True)
    reg('demonnano', 'deMon-nano', 'ase.calculators.demonnano.DemonNano',
        config=True)
    reg('dftb', 'DFTB+', 'ase.calculators.dftb.Dftb', config=True)
    reg('dftd3', 'DFT-D3', 'ase.calculators.dftd3.DFTD3', config=True)
    # reg('dftd3-pure', 'DFT-D3 (pure)', 'ase.calculators.dftd3.PureDFTD3')
    reg('dmol', 'DMol3', 'ase.calculators.dmol.DMol3', config=True)
    reg('eam', 'EAM', 'ase.calculators.eam.EAM')
    reg('eiqmmmm', 'Explicit interaction QMMM (wrapper)',
        'ase.calculators.qmmm.EIQMMM')
    reg('elk', 'ELK', 'ase.calculators.elk.ELK', config=True)
    reg('emt', 'EMT potential', 'ase.calculators.emt.EMT')
    reg('espresso', 'Quantum Espresso',
        'ase.calculators.espresso.EspressoTemplate', config=True)
    reg('exciting', 'Exciting',
        'ase.calculators.exciting.exciting.ExcitingGroundStateTemplate',
        config=True)
    reg('ff', 'FF', 'ase.calculators.ff.ForceField')
    reg('fd', 'Finite Difference (wrapper)',
        'ase.calculators.fd.FiniteDifferenceCalculator')
    reg('forceconstant', 'ForceConstantCalculator',
        'ase.calculators.qmmm.ForceConstantCalculator')
    reg('force-qmmmm', 'Force-based QM/MM Calculator (wrapper)',
        'ase.calculators.qmmm.ForceQMMM')
    reg('gamess_us', 'GAMESS-US', 'ase.calculators.gamess_us.GAMESSUS',
        config=True)
    reg('gaussian', 'Gaussian', 'ase.calculators.gaussian.Gaussian',
        config=True)
    reg('gromacs', 'Gromacs', 'ase.calculators.gromacs.Gromacs', config=True)
    reg('gulp', 'GULP', 'ase.calculators.gulp.GULP', config=True)
    reg('harmonic', 'Harmonic potential',
        'ase.calculators.harmonic.HarmonicCalculator')
    reg('idealgas', 'Ideal gas (dummy)',
        'ase.calculators.idealgas.IdealGas')
    reg('lammpslib', 'Lammps (python library)',
        'ase.calculators.lammpslib.LAMMPSlib', config=True)
    reg('lammpsrun', 'Lammps (external)',
        'ase.calculators.lammpsrun.LAMMPS', config=True)
    reg('linearcombination', 'LinearCombinationCalculator (wrapper)',
        'ase.calculators.mixing.LinearCombinationCalculator')
    reg('lj', 'Lennard–Jones potential',
        'ase.calculators.lj.LennardJones')
    reg('logging', 'LoggingCalculator (wrapper)',
        'ase.calculators.loggingcalc.LoggingCalculator')
    reg('mixed', 'MixedCalculator (wrapper)',
        'ase.calculators.mixing.MixedCalculator')
    reg('mopac', 'MOPAC', 'ase.calculators.mopac.MOPAC', config=True)
    reg('morse', 'Morse potential',
        'ase.calculators.morse.MorsePotential')
    reg('nwchem', 'NWChem', 'ase.calculators.nwchem.NWChem', config=True)
    reg('octopus', 'Octopus', 'ase.calculators.octopus.OctopusTemplate',
        config=True)
    reg('onetep', 'Onetep', 'ase.calculators.onetep.OnetepTemplate',
        config=True)
    reg('openmx', 'OpenMX', 'ase.calculators.openmx.OpenMX', config=True)
    reg('orca', 'ORCA', 'ase.calculators.orca.OrcaTemplate', config=True)
    reg('plumed', 'Plumed', 'ase.calculators.plumed.Plumed', config=True)
    reg('psi4', 'Psi4', 'ase.calculators.psi4.Psi4', config=True)
    reg('python-subprocess', 'PythonSubProcessCalculator',
        'ase.calculators.subprocesscalculator.PythonSubProcessCalculator')
    reg('qchem', 'QChem', 'ase.calculators.qchem.QChem', config=True)
    reg('rescaled', 'Rescaled Calculator (wrapper)',
        'ase.calculators.qmmm.RescaledCalculator')
    reg('siesta', 'SIESTA', 'ase.calculators.siesta.Siesta', config=True)
    reg('simple-qmmmm', 'Simple QMMM (wrapper)',
        'ase.calculators.qmmm.SimpleQMMM')
    reg('singlepoint', 'SinglePoint',
        'ase.calculators.singlepoint.SinglePointCalculator')
    reg('singlepoint-dft', 'SinglePointDFTCalculator',
        'ase.calculators.singlepoint.SinglePointDFTCalculator')
    reg('socketio', 'SocketIOCalculator (wrapper)',
        'ase.calculators.socketio.SocketIOCalculator')
    reg('spring', 'Spring Calculator',
        'ase.calculators.harmonic.SpringCalculator')
    reg('sum', 'jsumCalculator (wrapper)',
        'ase.calculators.mixing.SumCalculator')
    reg('tersoff', 'Tersoff potential',
        'ase.calculators.tersoff.Tersoff')
    reg('tip3p', 'TIP3P', 'ase.calculators.tip3p.TIP3P')
    reg('tip4p', 'TIP4P', 'ase.calculators.tip4p.TIP4P')
    reg('turbomole', 'Turbomole', 'ase.calculators.turbomole.Turbomole',
        config=True)
    reg('vasp', 'VASP', 'ase.calculators.vasp.Vasp', config=True)
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
