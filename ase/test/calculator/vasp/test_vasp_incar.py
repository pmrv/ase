# from os.path import join
from unittest import mock

import numpy as np
import pytest

from ase.atoms import Atoms
from ase.calculators.vasp import Vasp
from ase.calculators.vasp.create_input import GenerateVaspInput


@pytest.fixture()
def vaspinput_factory():
    """Factory for GenerateVaspInput class, which mocks the generation of
    pseudopotentials."""

    def _vaspinput_factory(**kwargs) -> GenerateVaspInput:
        mocker = mock.Mock()
        inputs = GenerateVaspInput()
        inputs.set(**kwargs)
        inputs._build_pp_list = mocker(  # type: ignore[method-assign]
            return_value=None
        )
        return inputs

    return _vaspinput_factory


def check_written_incar(parameters, expected_output, vaspinput_factory, tmpdir):
    atoms = Atoms('H2', positions=[[0, 0, 0], [0, 0, 1.2]])
    calc_factory = vaspinput_factory(**parameters)
    calc_factory.initialize(atoms)
    calc_factory.write_incar(atoms, tmpdir)
    with open(tmpdir / 'INCAR') as written_incar:
        assert written_incar.read() == expected_output


def test_str_key(vaspinput_factory, tmpdir):
    parameters = {'prec': 'Low'}
    expected_output = 'PREC = Low\n'
    check_written_incar(parameters, expected_output, vaspinput_factory, tmpdir)


def test_special_str_key(vaspinput_factory, tmpdir):
    parameters = {'xc': 'PBE'}
    expected_output = 'GGA = PE\n'
    check_written_incar(parameters, expected_output, vaspinput_factory, tmpdir)


def test_float_key(vaspinput_factory, tmpdir):
    parameters = {'encut': 400.0}
    expected_output = 'ENCUT = 400.000000\n'
    check_written_incar(parameters, expected_output, vaspinput_factory, tmpdir)


def test_exp_key(vaspinput_factory, tmpdir):
    parameters = {'ediff': 1e-6}
    expected_output = 'EDIFF = 1.00e-06\n'
    check_written_incar(parameters, expected_output, vaspinput_factory, tmpdir)


def test_int_key(vaspinput_factory, tmpdir):
    parameters = {'ibrion': 2}
    expected_output = 'IBRION = 2\n'
    check_written_incar(parameters, expected_output, vaspinput_factory, tmpdir)


def test_list_bool_key(vaspinput_factory, tmpdir):
    parameters = {'lattice_constraints': [False, True, False]}
    expected_output = 'LATTICE_CONSTRAINTS = .FALSE. .TRUE. .FALSE.\n'
    check_written_incar(parameters, expected_output, vaspinput_factory, tmpdir)


def test_bool_key(vaspinput_factory, tmpdir):
    parameters = {'lhfcalc': True}
    expected_output = 'LHFCALC = .TRUE.\n'
    check_written_incar(parameters, expected_output, vaspinput_factory, tmpdir)


def test_special_key(vaspinput_factory, tmpdir):
    parameters = {'lreal': True}
    expected_output = 'LREAL = .TRUE.\n'
    check_written_incar(parameters, expected_output, vaspinput_factory, tmpdir)


def test_list_float_key(vaspinput_factory, tmpdir):
    parameters = {'magmom': [0.5, 1.5]}
    expected_output = (
        'MAGMOM = 1*0.5000 1*1.5000\nISPIN = 2\n'  # Writer uses :.4f
    )
    check_written_incar(parameters, expected_output, vaspinput_factory, tmpdir)


def test_dict_key(
    vaspinput_factory, tmpdir
):  # dict key. Current writer uses %.3f
    parameters = {'ldau_luj': {'H': {'L': 2, 'U': 4.0, 'J': 0.0}}}
    expected_output = 'LDAU = .TRUE.\nLDAUL = 2\nLDAUU = 4.000\nLDAUJ = 0.000\n'
    check_written_incar(parameters, expected_output, vaspinput_factory, tmpdir)


def test_m_constr_key(vaspinput_factory, tmpdir) -> None:
    parameters = {
        'm_constr': [[0.0, 0.0, 1.5], [1.5, 0.0, 0.0]],
        'lnoncollinear': True,
    }
    expected_output = (
        'M_CONSTR = 2*0.0000 2*1.5000 2*0.0000\nLNONCOLLINEAR = .TRUE.\n'
    )
    check_written_incar(parameters, expected_output, vaspinput_factory, tmpdir)


@pytest.mark.parametrize('key', ['encut', 'npar', 'magmom'])
def test_unset_parameter(key, tmp_path):
    calc = Vasp(**{key: None})
    atoms = Atoms('H')
    calc.sort = [0]
    calc._set_spinpol(atoms)
    calc.write_incar(atoms, directory=tmp_path)
    assert key not in calc.asdict()['inputs']
    assert key.upper() not in (tmp_path / 'INCAR').read_text()


@pytest.mark.parametrize('dtype', [np.int32, np.int64, np.uint64])
def test_numpy_integer(dtype, tmp_path):
    calc = Vasp(encut=dtype(520), new_list=np.array([1, 2], dtype=dtype))
    atoms = Atoms('H')
    calc.sort = [0]
    calc._set_spinpol(atoms)
    calc.write_incar(atoms, directory=tmp_path)
    assert calc.encut == 520
    assert 'ENCUT = 520\n' in (tmp_path / 'INCAR').read_text()
    assert 'NEW_LIST = 1 2\n' in (tmp_path / 'INCAR').read_text()


@pytest.mark.parametrize('dtype', [int, np.int32, np.int64, float])
@pytest.mark.parametrize('ispin', [None, 1, 2])
def test_magmom_processing(dtype, ispin, tmp_path):
    atoms = Atoms('FeNiFe')
    magmom = np.array([1, -1, 2], dtype=dtype)
    kwargs = {} if ispin is None else {'ispin': ispin}
    calc = Vasp(magmom=magmom, **kwargs)
    calc.sort, calc.resort = calc._make_sort(atoms)
    calc._set_spinpol(atoms)
    calc.write_incar(atoms, directory=tmp_path)
    incar = (tmp_path / 'INCAR').read_text()
    assert f'ISPIN = {2 if ispin is None else ispin}\n' in incar
    assert 'MAGMOM = 1*1.0000 1*2.0000 1*-1.0000\n' in incar


def test_magmom_integer_list(tmp_path):
    atoms = Atoms('FeNiFe')
    calc = Vasp(magmom=[1, -1, 2])
    calc.sort, calc.resort = calc._make_sort(atoms)
    calc._set_spinpol(atoms)
    calc.write_incar(atoms, directory=tmp_path)
    incar = (tmp_path / 'INCAR').read_text()
    assert 'ISPIN = 2\n' in incar
    assert 'MAGMOM = 1*1.0000 1*2.0000 1*-1.0000\n' in incar


@pytest.mark.parametrize('dtype', [int, float])
def test_noncollinear_integer_magmoms(dtype, tmp_path):
    atoms = Atoms('FeNiFe')
    moments = np.eye(3, dtype=dtype)
    calc = Vasp(magmom=moments, m_constr=moments, lnoncollinear=True)
    calc.sort, calc.resort = calc._make_sort(atoms)
    calc._set_spinpol(atoms)
    calc.write_incar(atoms, directory=tmp_path)
    incar = (tmp_path / 'INCAR').read_text()
    sorted_moments = '1*1.0000 4*0.0000 1*1.0000 1*0.0000 1*1.0000 1*0.0000'
    assert f'MAGMOM = {sorted_moments}\n' in incar
    assert f'M_CONSTR = {sorted_moments}\n' in incar
    assert 'ISPIN' not in incar
