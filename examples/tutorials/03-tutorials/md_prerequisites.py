from ase.utils.sphinx_assert import SphinxPrerequisitesError

try:
    import asap3
except ImportError as e:
    raise SphinxPrerequisitesError from e
