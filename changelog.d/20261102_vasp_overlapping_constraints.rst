Bugfixes
--------

- The VASP writer now combines overlapping supported constraints on the same
  atom, preserving all fixed degrees of freedom in the selective-dynamics
  flags instead of keeping only the last constraint (:issue:`2055`).
