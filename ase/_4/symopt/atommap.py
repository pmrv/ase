import numpy as np

from ase import Atoms


def build_one_atommap(
    atoms1: Atoms,
    atoms2: Atoms,
    tol: float = 1e-12,
    min_atomdist: float = 0.5,
) -> tuple[list[int], float]:
    from ase.geometry import find_mic

    maxerr = 0.0
    atommap_a = []
    assert len(atoms1) == len(atoms2)
    for a in range(len(atoms1)):
        _, distances = find_mic(
            atoms2.positions[a] - atoms1.positions,
            cell=atoms1.cell,
            pbc=atoms1.pbc,
        )
        dist_indices = np.argsort(distances)
        atommap_a.append(dist_indices[0])
        sorted_distances = distances[dist_indices]
        mindist = sorted_distances[0]
        assert mindist < tol, f'Symmetry-mapped position off by {mindist}'
        if len(sorted_distances) > 1:
            # (This assertion may trigger if input structure is bad)
            assert sorted_distances[1] > min_atomdist, (
                'atoms suspiciously close'
            )

        assert atoms2.symbols[a] == atoms1.symbols[dist_indices[0]]
        maxerr = max(mindist, maxerr)
    return atommap_a, maxerr


def build_atommaps(
    atoms,
    dataset,
    tol: float = 1e-12,
    min_atomdist: float = 0.5,
) -> tuple[np.ndarray, float]:
    assert len(dataset.rotations) == len(dataset.translations)
    atommap_sa = []
    maxerr = 0.0

    orig_spos = atoms.get_scaled_positions(wrap=False)
    mapped_atoms = atoms.copy()

    for rot, trans in zip(dataset.rotations, dataset.translations):
        newspos = orig_spos @ rot.T + trans[None, :]
        mapped_atoms.positions[:] = atoms.cell.cartesian_positions(newspos)

        atommap, maxerr1 = build_one_atommap(
            atoms, mapped_atoms, tol, min_atomdist
        )
        atommap_sa.append(atommap)
        maxerr = max(maxerr, maxerr1)
    return np.array(atommap_sa, int), maxerr
