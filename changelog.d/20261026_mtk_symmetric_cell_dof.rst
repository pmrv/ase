Bugfixes
--------

- Fix excessive volume fluctuations in
  :class:`~ase.md.nose_hoover_chain.MTKNPT` by using six cell momentum degrees
  of freedom instead of nine in the barostat thermostat
  (:issue:`2024`, :mr:`4303`).
