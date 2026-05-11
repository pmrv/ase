.. A new scriv changelog fragment.
..
.. Uncomment the section that is right (remove the leading dots).
.. For top level release notes, leave all the headers commented out.
..
.. I/O
.. ---
..
.. - A bullet item for the I/O category.
..
Calculators
-----------

- :class:`~ase.calculators.socketio.SocketIOCalculator`:
  The :class:`~ase.calculators.socketio.SocketClient` now goes into
  the “ready” state after computing forces whereas previously it would
  request a reinitialization.
  This change ensures future compatibility with the driver as
  implemented in `i-pi <https://ipi-code.org/>`__
  and may be significantly faster in larger, fast-running
  computations (e.g. with MLIPs). (:mr:`4069`)


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
