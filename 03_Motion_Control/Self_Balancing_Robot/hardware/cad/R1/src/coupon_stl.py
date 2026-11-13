"""Generate watertight STL test coupons: a plate made of square cells, each cell
either solid or with one round through-hole. No CAD kernel needed.

Each cell's outer square and hole circle are sampled at the same N angles
(N multiple of 8 so square corners are hit exactly), giving a clean quad-strip
triangulation. Adjacent cells share identical edge points, so the mesh is
manifold. Boundary edges of the top face are extruded into walls.
"""
import math
import struct
import sys
from collections import Counter


def cell_top_tris(cx, cy, s, d, n):
    h = s / 2.0
    ring_b, ring_h = [], []
    for k in range(n):
        t = 2 * math.pi * k / n
        c, si = math.cos(t), math.sin(t)
        m = h / max(abs(c), abs(si))
        ring_b.append((cx + m * c, cy + m * si))
        if d:
            ring_h.append((cx + d / 2 * c, cy + d / 2 * si))
    tris = []
    for k in range(n):
        k1 = (k + 1) % n
        if d:
            tris.append((ring_h[k], ring_b[k], ring_b[k1]))
            tris.append((ring_h[k], ring_b[k1], ring_h[k1]))
        else:
            tris.append(((cx, cy), ring_b[k], ring_b[k1]))
    return tris


def key(p):
    return (round(p[0], 5), round(p[1], 5))


def build(cells, s, n, thick):
    """cells: list of hole diameters (0 = solid), laid out left to right."""
    top = []
    for i, d in enumerate(cells):
        top += cell_top_tris(s / 2 + i * s, s / 2, s, d, n)
    top = [tuple(key(p) for p in t) for t in top]
    # drop degenerate (corner rays produce none, but be safe)
    top = [t for t in top if len({t[0], t[1], t[2]}) == 3]

    und = Counter()
    for a, b, c in top:
        for u, v in ((a, b), (b, c), (c, a)):
            und[frozenset((u, v))] += 1
    faces = []
    for a, b, c in top:
        faces.append(((*a, thick), (*b, thick), (*c, thick)))
        faces.append(((*a, 0.0), (*c, 0.0), (*b, 0.0)))
        for u, v in ((a, b), (b, c), (c, a)):
            if und[frozenset((u, v))] == 1:
                ub, vb, vt, ut = (*u, 0.0), (*v, 0.0), (*v, thick), (*u, thick)
                faces.append((ub, vb, vt))
                faces.append((ub, vt, ut))
    return faces


def check(faces):
    directed = Counter()
    for f in faces:
        for i in range(3):
            directed[(f[i], f[(i + 1) % 3])] += 1
    bad = sum(1 for (u, v), c in directed.items() if c != 1 or directed.get((v, u), 0) != 1)
    vol = 0.0
    for a, b, c in faces:
        vol += (a[0] * (b[1] * c[2] - b[2] * c[1])
                - a[1] * (b[0] * c[2] - b[2] * c[0])
                + a[2] * (b[0] * c[1] - b[1] * c[0])) / 6.0
    return bad, vol


def write_stl(path, faces, name):
    with open(path, "wb") as f:
        f.write(name.encode()[:80].ljust(80, b" "))
        f.write(struct.pack("<I", len(faces)))
        for a, b, c in faces:
            ux, uy, uz = (b[i] - a[i] for i in range(3))
            vx, vy, vz = (c[i] - a[i] for i in range(3))
            nx, ny, nz = uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx
            L = math.sqrt(nx * nx + ny * ny + nz * nz) or 1.0
            f.write(struct.pack("<12fH", nx / L, ny / L, nz / L, *a, *b, *c, 0))


if __name__ == "__main__":
    out = sys.argv[1]
    jobs = [
        # name, cells (hole dia, 0 = solid marker), cell size, segments, thickness
        ("coupon_switch_D19.5_20.0_20.5_t2.0", [0, 19.5, 20.0, 20.5], 30.0, 96, 2.0),
        ("coupon_M3_D2.5_3.2_3.4_3.6_4.0_4.2_t6", [0, 2.5, 3.2, 3.4, 3.6, 4.0, 4.2], 12.0, 48, 6.0),
    ]
    for name, cells, s, n, t in jobs:
        faces = build(cells, s, n, t)
        bad, vol = check(faces)
        write_stl(f"{out}/{name}.stl", faces, name)
        expect = len(cells) * s * s * t - sum(math.pi * d * d / 4 * t for d in cells)
        print(f"{name}: {len(faces)} tris, non-manifold edges={bad}, vol={vol:.1f} mm^3 "
              f"(analytic ~{expect:.1f}), size {len(cells)*s:g} x {s:g} x {t:g} mm")
