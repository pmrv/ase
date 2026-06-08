"""Prerequisites - skips the gallery script if not met."""

from ase.utils.sphinx_assert import SphinxPrerequisitesError

# we need import asap3 to not fail
try:
    import asap3
except ImportError as e:
    raise SphinxPrerequisitesError from e
