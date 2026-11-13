"""Interference check + render for the R1 assembly."""
import itertools
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_r1  # noqa: E402

out = sys.argv[1]
solids, _, _ = build_r1.main(out)

# ---- interference ------------------------------------------------------
names = list(solids)
shapes = {n: solids[n].val() for n in names}
bbs = {n: shapes[n].BoundingBox() for n in names}


def bb_overlap(a, b, tol=0.01):
    return (a.xmin < b.xmax - tol and b.xmin < a.xmax - tol and a.ymin < b.ymax - tol
            and b.ymin < a.ymax - tol and a.zmin < b.zmax - tol and b.zmin < a.zmax - tol)


hits = []
for a, b in itertools.combinations(names, 2):
    if not bb_overlap(bbs[a], bbs[b]):
        continue
    v = shapes[a].intersect(shapes[b]).Volume()
    if v > 1.0:
        hits.append((a, b, round(v, 1)))
print("INTERFERENCES (>1 mm^3):")
for h in hits:
    print("  ", h)
if not hits:
    print("   none")

# ---- render --------------------------------------------------------------
colors = {"deck": "#4a7fb5", "column": "#b8b8b8", "tray": "#2a9d8f", "battery": "#1d3557",
          "carrier": "#f4a261", "board": "#2d6a4f", "switch": "#111111", "skid": "#f4a261",
          "bracket": "#777777", "motor": "#c0c0c0", "wheel": "#222222"}


def col(n):
    for k, c in colors.items():
        if k in n:
            return c
    return "#999999"


def draw(ax, elev, azim, title):
    light = np.array([0.4, -0.5, 0.8])
    light /= np.linalg.norm(light)
    for n in names:
        verts, tris = shapes[n].tessellate(0.5, 0.3)
        V = np.array([(v.x, v.y, v.z) for v in verts])
        T = np.array(tris)
        polys = V[T]
        nrm = np.cross(polys[:, 1] - polys[:, 0], polys[:, 2] - polys[:, 0])
        nrm /= (np.linalg.norm(nrm, axis=1, keepdims=True) + 1e-9)
        shade = 0.45 + 0.55 * np.clip(np.abs(nrm @ light), 0, 1)
        base = np.array(matplotlib.colors.to_rgb(col(n)))
        fc = np.clip(base[None, :] * shade[:, None], 0, 1)
        pc = Poly3DCollection(polys, facecolors=fc, edgecolors="none")
        ax.add_collection3d(pc)
    ax.set_xlim(-130, 130); ax.set_ylim(-130, 130); ax.set_zlim(-20, 240)
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev, azim)
    ax.set_axis_off()
    ax.set_title(title, fontsize=10)


fig = plt.figure(figsize=(14, 7))
draw(fig.add_subplot(1, 2, 1, projection="3d"), 22, -55, "R1 assembly (80 mm columns)")
draw(fig.add_subplot(1, 2, 2, projection="3d"), 0, 0, "Side view along axle (fall direction left-right)")
plt.tight_layout()
plt.savefig(os.path.join(out, "R1_render.png"), dpi=110)
print("render saved")
