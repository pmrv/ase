"""Prerequisites - skips the gallery script if not met."""

from ase.config import cfg
from ase.utils.sphinx_assert import SphinxPrerequisitesError

# we need cp2k_shell in cp2k config
if not cfg.parser.get('cp2k', 'cp2k_shell', fallback=None):
    raise SphinxPrerequisitesError('CP2K not configured in ase.config')
