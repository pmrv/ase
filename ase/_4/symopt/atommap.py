import numpy as np

from ase import Atoms


def build_one_atommap(
    atoms1: Atoms,
    atoms2: Atoms,
    maxerr: float = 1e-12,
    min_atomdist: float = 0.5,
) -> tuple[list[int], float]:
    from ase.geometry import find_mic

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
        assert mindist < maxerr, f'Symmetry-mapped position off by {mindist}'
        if len(sorted_distances) > 1:
            # (This assertion may trigger if input structure is bad)
            assert sorted_distances[1] > min_atomdist, (
                'atoms suspiciously close'
            )

        assert atoms2.symbols[a] == atoms1.symbols[dist_indices[0]]
    return atommap_a


def transform(scaled_positions, rotation, translation):
    # (Vectorize this for multiple ops some day)
    return scaled_positions @ rotation.T + translation[None, :]


def build_atommaps(
    atoms,
    dataset,
    maxerr: float = 1e-12,
    min_atomdist: float = 0.5,
) -> tuple[np.ndarray, float]:
    assert len(dataset.rotations) == len(dataset.translations)
    atommap_sa = []

    orig_spos = atoms.get_scaled_positions(wrap=False)
    mapped_atoms = atoms.copy()

    for rot, trans in zip(dataset.rotations, dataset.translations):
        newspos = transform(orig_spos, rot, trans)
        mapped_atoms.positions[:] = atoms.cell.cartesian_positions(newspos)

        atommap = build_one_atommap(atoms, mapped_atoms, maxerr, min_atomdist)
        atommap_sa.append(atommap)
    return np.array(atommap_sa, int)
