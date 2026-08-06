Other changes
-------------

- :class:`~ase.neighborlist.PrimitiveNeighborList` (the default cKDTree
  neighbour-list path used by :class:`~ase.neighborlist.NeighborList`) now
  assembles its results with vectorised array operations instead of a
  per-atom Python loop. This is roughly 2.5x faster to build for typical
  mid-to-large periodic systems; the returned neighbour lists are unchanged.
