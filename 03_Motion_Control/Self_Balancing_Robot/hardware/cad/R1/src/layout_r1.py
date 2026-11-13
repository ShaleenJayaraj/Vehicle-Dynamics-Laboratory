"""2D top-view layout drawing of both R1 decks (from params + build_r1 helpers)."""
import math
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_r1 as B  # noqa: E402
import params as P  # noqa: E402


def slot_patch(ax, x, y, L, w, ang, **kw):
    if ang == 90:
        ax.add_patch(FancyBboxPatch((x - w / 2, y - L / 2), w, L,
                                    boxstyle=f"round,pad=0,rounding_size={w/2}", **kw))
    else:
        ax.add_patch(FancyBboxPatch((x - L / 2, y - w / 2), L, w,
                                    boxstyle=f"round,pad=0,rounding_size={w/2}", **kw))


def rot(p, deg):
    a = math.radians(deg)
    return (p[0] * math.cos(a) - p[1] * math.sin(a), p[0] * math.sin(a) + p[1] * math.cos(a))


def board_overlay(ax, name):
    deck, (cx, cy), r = P.PLACEMENT[name]
    bd = P.BOARDS[name]
    w, h = (bd["w"], bd["h"]) if r % 180 == 0 else (bd["h"], bd["w"])
    ax.add_patch(Rectangle((cx - w / 2, cy - h / 2), w, h, fill=True, fc="#2d6a4f22",
                           ec="#2d6a4f", lw=1.2, ls="--"))
    for hx, hy in bd["holes"]:
        px, py = rot((hx, hy), r)
        ax.add_patch(Circle((cx + px, cy + py), P.STANDOFF_D / 2, fc="#f4a261", ec="k", lw=0.5))
    for mx, my in bd["mounts"]:
        px, py = rot((mx, my), r)
        ax.add_patch(Circle((cx + px, cy + py), 2.6, fc="none", ec="#e76f51", lw=1.5))
    tag = "" if bd["status"] != "PROVISIONAL" else "\n(PROVISIONAL holes)"
    ax.text(cx, cy, f"{name.upper()}{tag}", ha="center", va="center", fontsize=8, color="#1b4332")


def deck(ax, which):
    W, D = P.DECK_W, P.DECK_D
    ax.add_patch(FancyBboxPatch((-W / 2, -D / 2), W, D, boxstyle=f"round,pad=0,rounding_size={P.CORNER_R}",
                                fc="#dbe7f3", ec="#1d3557", lw=1.5))
    for x, y in B.column_pts():
        ax.add_patch(Circle((x, y), P.COLUMN_D / 2, fc="#cccccc", ec="k", lw=0.5, alpha=0.6))
        ax.add_patch(Circle((x, y), P.M3_CLEAR / 2, fc="white", ec="k", lw=0.5))
    excl = B.lower_excluded if which == "lower" else B.upper_excluded
    for x, y in B.grid_points(excl):
        ax.add_patch(Circle((x, y), P.M3_CLEAR / 2, fc="white", ec="#555", lw=0.4))
    if which == "lower":
        for it in B.bracket_slot_items():
            slot_patch(ax, *it, fc="white", ec="k", lw=0.8)
        for it in B.motor_wire_slot_items():
            slot_patch(ax, *it, fc="white", ec="k", lw=0.8)
        for sx in (-1, 1):
            ax.add_patch(Rectangle((sx * (W / 2) - (30 if sx > 0 else 0), -12), 30, 24, fill=False,
                                   ec="#888", ls=":", lw=1))
            mx0 = sx * (W / 2 - P.BRACKET_WALL)
            ax.add_patch(Rectangle((min(mx0, mx0 - sx * P.MOTOR_LEN), -P.MOTOR_D / 2), P.MOTOR_LEN,
                                   P.MOTOR_D, fill=False, ec="#999", ls=":", lw=1))
        ax.text(0, -66, "motors, brackets, skid feet mount underneath (dotted)", ha="center", fontsize=7, color="#555")
        for sx in (-1, 1):
            for sy in (-1, 1):
                ax.add_patch(Rectangle((sx * P.FOOT_X - 12, sy * P.FOOT_Y - 7), 24, 14, fill=False,
                                       ec="#f4a261", ls="-.", lw=1.2))
                for d in (-P.FOOT_HOLE_DX, P.FOOT_HOLE_DX):
                    ax.add_patch(Circle((sx * P.FOOT_X + d, sy * P.FOOT_Y), 2.6, fc="none", ec="#e76f51", lw=1.5))
    else:
        for x, y in P.UPPER_SLOTS:
            slot_patch(ax, x, y, P.UPPER_SLOT_L, P.UPPER_SLOT_W, 0, fc="white", ec="k", lw=0.8)
        sx, sy = P.SWITCH_XY
        ax.add_patch(Circle((sx, sy), P.SWITCH_POCKET_D / 2, fc="#eeeeee", ec="#888", ls="--", lw=0.8))
        ax.add_patch(Circle((sx, sy), P.SWITCH_HOLE / 2, fc="white", ec="k", lw=1))
        ax.text(sx, sy - 20, f"switch Ø{P.SWITCH_HOLE:g}\n(2 mm skin)", ha="center", fontsize=7)
        pin_x, pin_y, out_x, ear_y = B.tray_dims()
        ax.add_patch(Rectangle((-out_x, -ear_y), 2 * out_x, 2 * ear_y, fill=False, ec="#2a9d8f", lw=1.5))
        ax.add_patch(Rectangle((-P.BATT_W / 2, -pin_y + 0.5), P.BATT_W, P.BATT_L, fc="#1d355733", ec="#1d3557"))
        ax.text(0, 0, "BATTERY\n3S 2200\n(leads →+Y)", ha="center", va="center", fontsize=7, rotation=90)
    for b, (d, _, _) in P.PLACEMENT.items():
        if d == which:
            board_overlay(ax, b)
    ax.set_xlim(-W / 2 - 8, W / 2 + 8)
    ax.set_ylim(-D / 2 - 8, D / 2 + 8)
    ax.set_aspect("equal")
    ax.set_title(f"{which.upper()} deck — top view, {W:g} × {D:g} × {P.LOWER_T if which=='lower' else P.UPPER_T:g} mm"
                 f"   (grid {P.GRID_PITCH:g} mm, Ø{P.M3_CLEAR:g})", fontsize=10)
    ax.set_xlabel("X (axle) [mm]")
    ax.set_ylabel("Y (fore-aft) [mm]")
    ax.grid(False)


out = sys.argv[1]
fig, axes = plt.subplots(1, 2, figsize=(16, 7.5))
deck(axes[0], "lower")
deck(axes[1], "upper")
fig.text(0.5, 0.01, "Orange dots = board standoffs (pilot Ø2.5).  Red rings = carrier-to-deck M3 bolts.  "
         "Green dashed = board outline.  Columns at (±77, ±60).", ha="center", fontsize=9)
plt.tight_layout(rect=(0, 0.03, 1, 1))
plt.savefig(os.path.join(out, "R1_deck_layout.png"), dpi=120)
print("ok")
