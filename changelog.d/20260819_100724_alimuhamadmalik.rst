Bugfixes
--------

- Fixed VASP input generation so that ``MAGMOM`` and ``M_CONSTR`` are
  written correctly for non-collinear calculations with
  ``LNONCOLLINEAR = .TRUE.``. Also fixed magnetic-moment parsing so that
  all three components are read from ``OUTCAR`` for non-collinear
  calculations.
  (:mr:`3591`, :mr:`4205`)
