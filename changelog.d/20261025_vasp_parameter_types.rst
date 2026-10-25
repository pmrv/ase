Bugfixes
--------

- Restore VASP support for unset INCAR parameters and NumPy numeric inputs,
  and fix the ``encut`` property for integer and unset cutoffs. Preserve
  magnetic-moment processing for integer lists (:issue:`2025`,
  :issue:`2026`, :issue:`2027`, :issue:`2028`).
