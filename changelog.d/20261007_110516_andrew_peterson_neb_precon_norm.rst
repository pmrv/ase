Optimizers
----------

- ``Precon.apply()`` now returns only the preconditioned forces, not a
  ``(forces, residual)`` tuple. :class:`~ase.optimize.ODE12r` now computes
  its residual with the optimizable's own gradient norm, so it no longer
  depends on the number of degrees of freedom (:mr:`4093`)

Bugfixes
--------

- Fixed the residual of the preconditioned :class:`~ase.mep.neb.NEB`
  (``precon=...``) to use the maximum per-atom force norm, consistent with
  ``fmax`` elsewhere in ASE, rather than the largest single force component.
  The residual is now rotationally invariant, but convergence is slightly
  stricter (by at most a factor of √3), so runs with a hand-tuned ``fmax``
  may take a few more steps (:mr:`4093`)
