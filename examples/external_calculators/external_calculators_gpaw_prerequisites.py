"""Prerequisites for plot_something.py — skips the gallery script if not met."""

from ase.utils.sphinx_assert import SphinxPrerequisitesError

# we need import gpaw to not fail
try:
    import gpaw
except ImportError as e:
    raise SphinxPrerequisitesError from e
