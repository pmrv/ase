from ase.utils.sphinx_assert import SphinxPrerequisitesError

try:
    import gpaw
except ImportError as e:
    raise SphinxPrerequisitesError from e
