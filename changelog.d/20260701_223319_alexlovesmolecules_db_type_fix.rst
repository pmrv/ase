.. A new scriv changelog fragment.
..
.. Uncomment the section that is right (remove the leading dots).
.. For top level release notes, leave all the headers commented out.
..
I/O
---

- :mod:`ase.db`: Guarantee dtypes match in `blob`/`deblob`. Prompted by
  FAIRChem's calculator writing float32 forces, which were saved as bytes by
  `blob` and then reinterpreted as float64 by `deblob`. Now, `blob` takes a
  `dtype` argument, matching what `deblob` will read it as for each field.
  Types are cast if numpy's same_kind rule allows it; otherwise, a ValueError
  is raised.

.. Calculators
.. -----------
..
.. - A bullet item for the Calculators category.
..
.. Optimizers
.. ----------
..
.. - A bullet item for the Optimizers category.
..
.. Molecular dynamics
.. ------------------
..
.. - A bullet item for the Molecular dynamics category.
..
.. GUI
.. ---
..
.. - A bullet item for the GUI category.
..
.. Development
.. -----------
..
.. - A bullet item for the Development category.
..
.. Documentation
.. -------------
..
.. - A bullet item for the Documentation category.
..
.. Other changes
.. -------------
..
.. - A bullet item for the Other changes category.
..
.. Bugfixes
.. --------
..
.. - A bullet item for the Bugfixes category.
..
