"""Build R1 chassis parts for the self-balancing robot (CadQuery).

    python build_r1.py [out_dir]

Writes one STEP + STL per printable part, an assembly STEP (with simple
stand-ins for motors, wheels, boards and battery) and a parts summary.
All dimensions come from params.py.
"""
import json
import math
import os
import sys

import cadquery as cq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import params as P  # noqa: E402


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def cylinders(points, d, h, z0=0.0):
    """Union of vertical cylinders (used as cutters)."""
    if not points:
        return None
    return (cq.Workplane("XY").workplane(offset=z0)
            .pushPoints(points).circle(d / 2.0).extrude(h))


def slots(items, h, z0=0.0):
    """items: (x, y, length_end_to_end, width, angle_deg)."""
    wp = None
    for x, y, L, w, ang in items:
        s = (cq.Workplane("XY").workplane(offset=z0).center(x, y)
             .slot2D(L, w, ang).extrude(h))
        wp = s if wp is None else wp.union(s)
    return wp


def cut_all(body, cutters):
    for c in cutters:
        if c is not None:
            body = body.cut(c)
    return body


def plate(w, d, t, r):
    return (cq.Workplane("XY").box(w, d, t, centered=(True, True, False))
            .edges("|Z").fillet(r))


def column_pts():
    cx, cy = P.COLUMN_XY
    return [(sx * cx, sy * cy) for sx in (-1, 1) for sy in (-1, 1)]


def grid_points(excluded):
    pts = []
    n_x = int(P.GRID_X_MAX // P.GRID_PITCH)
    n_y = int(P.GRID_Y_MAX // P.GRID_PITCH)
    for i in range(-n_x, n_x + 1):
        for j in range(-n_y, n_y + 1):
            x, y = i * P.GRID_PITCH, j * P.GRID_PITCH
            if not excluded(x, y):
                pts.append((x, y))
    return pts


def near_column(x, y, r=11.0):
    return any(math.hypot(x - cx, y - cy) < r for cx, cy in column_pts())


# --------------------------------------------------------------------------
# lower deck
# --------------------------------------------------------------------------
def bracket_slot_items():
    x0, x1 = P.BRACKET_SLOT_X
    L = (x1 - x0) + P.M3_CLEAR
    xc = (x0 + x1) / 2.0
    hy = P.BRACKET_HOLES_Y / 2.0
    return [(sx * xc, sy * hy, L, P.M3_CLEAR, 0.0) for sx in (-1, 1) for sy in (-1, 1)]


def motor_wire_slot_items():
    s = P.MOTOR_WIRE_SLOT
    return [(sx * s["x"], 0.0, s["l"], s["w"], 90.0) for sx in (-1, 1)]


def lower_excluded(x, y):
    if near_column(x, y):
        return True
    if abs(x) >= 48 and abs(y) <= 16:                     # bracket slots
        return True
    s = P.MOTOR_WIRE_SLOT
    if abs(abs(x) - s["x"]) <= s["w"] / 2 + 4 and abs(y) <= s["l"] / 2 + 4:
        return True
    return False


def lower_deck():
    t = P.LOWER_T
    body = plate(P.DECK_W, P.DECK_D, t, P.CORNER_R)
    cutters = [
        cylinders(column_pts(), P.M3_CLEAR, t + 2, -1),
        cylinders(grid_points(lower_excluded), P.M3_CLEAR, t + 2, -1),
        slots(bracket_slot_items(), t + 2, -1),
        slots(motor_wire_slot_items(), t + 2, -1),
    ]
    return cut_all(body, cutters)


# --------------------------------------------------------------------------
# upper deck
# --------------------------------------------------------------------------
def upper_excluded(x, y):
    if near_column(x, y):
        return True
    sx, sy = P.SWITCH_XY
    if math.hypot(x - sx, y - sy) < P.SWITCH_POCKET_D / 2 + 5:
        return True
    for ux, uy in P.UPPER_SLOTS:
        if abs(x - ux) <= P.UPPER_SLOT_L / 2 + 4 and abs(y - uy) <= P.UPPER_SLOT_W / 2 + 4:
            return True
    return False


def upper_deck():
    t = P.UPPER_T
    body = plate(P.DECK_W, P.DECK_D, t, P.CORNER_R)
    sx, sy = P.SWITCH_XY
    pocket_depth = t - P.SWITCH_SKIN
    cutters = [
        cylinders(column_pts(), P.M3_CLEAR, t + 2, -1),
        cylinders(grid_points(upper_excluded), P.M3_CLEAR, t + 2, -1),
        slots([(x, y, P.UPPER_SLOT_L, P.UPPER_SLOT_W, 0.0) for x, y in P.UPPER_SLOTS], t + 2, -1),
        cylinders([(sx, sy)], P.SWITCH_HOLE, t + 2, -1),
        cylinders([(sx, sy)], P.SWITCH_POCKET_D, pocket_depth + 1, -1),   # from underside
    ]
    return cut_all(body, cutters)


# --------------------------------------------------------------------------
# columns
# --------------------------------------------------------------------------
def column(length):
    return (cq.Workplane("XY").circle(P.COLUMN_D / 2).circle(P.M3_PILOT / 2)
            .extrude(length).edges().chamfer(0.5))


# --------------------------------------------------------------------------
# battery tray (long axis along Y, open lead end at +Y)
# --------------------------------------------------------------------------
def tray_dims():
    pin_x = P.BATT_W / 2 + P.BATT_CLEAR              # pocket half-width
    pin_y = P.BATT_L / 2 + P.BATT_CLEAR              # pocket half-length
    out_x = pin_x + P.TRAY_WALL_T
    ear_y = P.TRAY_EAR_Y + 5.0
    return pin_x, pin_y, out_x, ear_y


def battery_tray():
    pin_x, pin_y, out_x, ear_y = tray_dims()
    b = P.TRAY_BASE_T
    body = (cq.Workplane("XY").box(2 * out_x, 2 * ear_y, b, centered=(True, True, False))
            .edges("|Z").fillet(3))
    wall_len = 2 * pin_y + P.TRAY_WALL_T            # from end wall to open end
    wall_yc = -P.TRAY_WALL_T / 2                    # shifted so open end is at +pin_y
    for sx in (-1, 1):
        w = (cq.Workplane("XY").workplane(offset=b)
             .center(sx * (pin_x + P.TRAY_WALL_T / 2), wall_yc)
             .box(P.TRAY_WALL_T, wall_len, P.TRAY_WALL_H, centered=(True, True, False)))
        body = body.union(w)
    end = (cq.Workplane("XY").workplane(offset=b)
           .center(0, -(pin_y + P.TRAY_WALL_T / 2))
           .box(2 * out_x, P.TRAY_WALL_T, P.TRAY_WALL_H, centered=(True, True, False)))
    body = body.union(end)
    holes = [(sx * 10.0, sy * P.TRAY_EAR_Y) for sx in (-1, 1) for sy in (-1, 1)]
    grooves = None
    for sy in (-1, 1):
        g = (cq.Workplane("XY").workplane(offset=-1).center(0, sy * P.STRAP_GROOVE_Y)
             .box(2 * out_x + 2, P.STRAP_GROOVE_W, P.STRAP_GROOVE_DEPTH + 1,
                  centered=(True, True, False)))
        grooves = g if grooves is None else grooves.union(g)
    return cut_all(body, [cylinders(holes, P.M3_CLEAR, b + 2, -1), grooves])


# --------------------------------------------------------------------------
# board carriers
# --------------------------------------------------------------------------
def carrier(name):
    bd = P.BOARDS[name]
    t = P.CARRIER_T
    mx = max(abs(m[0]) for m in bd["mounts"])
    my = max(abs(m[1]) for m in bd["mounts"])
    hx = max(bd["w"] / 2 + P.CARRIER_MARGIN, mx + 5)
    hy = max(bd["h"] / 2 + P.CARRIER_MARGIN, my + 5)
    body = plate(2 * hx, 2 * hy, t, 3)
    sh = bd["standoff_h"]
    so = cylinders(bd["holes"], P.STANDOFF_D, sh, t)
    body = body.union(so)
    if bd.get("support"):
        body = body.union(cylinders(bd["support"], 5.0, sh, t))
    # lighten: window under the board centre where nothing is mounted
    win_x = min(bd["w"] / 2 - 8, mx - 9)
    win_y = min(bd["h"] / 2 - 8, hy - 6)
    cutters = [cylinders(bd["holes"], P.M3_PILOT, t + sh + 2, -1),
               cylinders(bd["mounts"], P.M3_CLEAR, t + 2, -1)]
    if win_x > 6 and win_y > 6:
        cutters.append(cq.Workplane("XY").workplane(offset=-1)
                       .rect(2 * win_x, 2 * win_y).extrude(t + 2)
                       .edges("|Z").fillet(3))
    return cut_all(body, cutters)


# --------------------------------------------------------------------------
# skid foot / rest stand
# --------------------------------------------------------------------------
def foot_length():
    r = P.WHEEL_D / 2
    th = math.radians(P.REST_ANGLE_DEG)
    dz = (P.FOOT_Y * math.sin(th) - r) / math.cos(th)   # tip height rel. axle
    return P.AXLE_BELOW_DECK - dz                        # below deck underside


def skid_foot():
    L = foot_length()
    top = (cq.Workplane("XY").box(24, 14, 5, centered=(True, True, False))
           .translate((0, 0, -5)).edges("|Z").fillet(3))
    leg = (cq.Workplane("XY").box(P.FOOT_W, P.FOOT_T, L - 5, centered=(True, True, False))
           .translate((0, 0, -L)))
    leg = leg.edges("<Z").fillet(3)
    body = top.union(leg)
    d = P.FOOT_HOLE_DX
    return cut_all(body, [cylinders([(-d, 0), (d, 0)], P.M3_PILOT, 6, -5.5)])


# --------------------------------------------------------------------------
# stand-ins for the assembly
# --------------------------------------------------------------------------
def standins(z_lower, z_upper):
    r = P.WHEEL_D / 2
    z_ax = r
    items = []
    edge = P.DECK_W / 2
    for sx in (-1, 1):
        # bracket (flange + vertical plate), approx
        fl = cq.Workplane("XY").box(30, 24, 2.5, centered=(True, True, False)).translate(
            (sx * (edge - 15), 0, z_lower - 2.5))
        vp = cq.Workplane("XY").box(P.BRACKET_WALL, 24, z_lower - (z_ax - 12)).translate(
            (sx * (edge - P.BRACKET_WALL / 2), 0, (z_lower + z_ax - 12) / 2))
        items.append((f"bracket_{'R' if sx > 0 else 'L'}", fl.union(vp), "gray"))
        m = (cq.Workplane("YZ").circle(P.MOTOR_D / 2).extrude(P.MOTOR_LEN)
             .translate((sx * (edge - P.BRACKET_WALL) - (P.MOTOR_LEN if sx > 0 else 0), 0, z_ax)))
        items.append((f"motor_{'R' if sx > 0 else 'L'}", m, "gray"))
        wx = sx * (edge + P.WHEEL_GAP + P.WHEEL_W / 2)
        w = (cq.Workplane("YZ").circle(r).circle(r - 8).extrude(P.WHEEL_W)
             .translate((wx - P.WHEEL_W / 2, 0, z_ax)))
        items.append((f"wheel_{'R' if sx > 0 else 'L'}", w, "black"))
    return items


def board_standin(name):
    bd = P.BOARDS[name]
    comp_h = {"uno": 12, "xy160d": 25, "zx052": 15, "gy521": 3}[name]
    b = cq.Workplane("XY").box(bd["w"], bd["h"], 1.6, centered=(True, True, False))
    c = (cq.Workplane("XY").box(bd["w"] * 0.7, bd["h"] * 0.7, comp_h,
                                centered=(True, True, False)).translate((0, 0, 1.6)))
    return b.union(c)


def place(wp, xy, z, rot):
    return wp.rotate((0, 0, 0), (0, 0, 1), rot).translate((xy[0], xy[1], z))


# --------------------------------------------------------------------------
def main(out):
    os.makedirs(out, exist_ok=True)
    parts = {
        "01_lower_deck": (lower_deck(), 1),
        "02_upper_deck": (upper_deck(), 1),
        "04_battery_tray": (battery_tray(), 1),
        "05_carrier_uno": (carrier("uno"), 1),
        "06_carrier_xy160d": (carrier("xy160d"), 1),
        "07_carrier_zx052": (carrier("zx052"), 1),
        "08_carrier_gy521_imu": (carrier("gy521"), 1),
        "09_skid_foot": (skid_foot(), 4),
    }
    for L in P.COLUMN_LENGTHS:
        parts[f"03_column_L{int(L)}"] = (column(L), 4)

    # STEP = assembly orientation (for CAD). STL = print orientation (for slicer).
    flip_for_print = {"02_upper_deck", "09_skid_foot"}   # switch pocket / foot plate on bed
    summary = {}
    for name, (wp, qty) in sorted(parts.items()):
        cq.exporters.export(wp, os.path.join(out, f"{name}.step"))
        pw = wp.rotate((0, 0, 0), (1, 0, 0), 180) if name in flip_for_print else wp
        cq.exporters.export(pw, os.path.join(out, f"{name}.stl"), tolerance=0.02, angularTolerance=0.1)
        bb = wp.val().BoundingBox()
        vol = wp.val().Volume()
        summary[name] = dict(qty=qty, bbox=[round(bb.xlen, 1), round(bb.ylen, 1), round(bb.zlen, 1)],
                             volume_cm3=round(vol / 1000, 2),
                             solid_mass_abs_g=round(vol / 1000 * 1.04, 1),
                             valid=wp.val().isValid())

    # ---- assembly -------------------------------------------------------
    z_low = P.WHEEL_D / 2 + P.AXLE_BELOW_DECK
    z_col = z_low + P.LOWER_T
    z_up = z_col + P.COLUMN_DEFAULT
    z_up_top = z_up + P.UPPER_T
    asm = cq.Assembly(name="R1")
    solids = {}

    def add(name, wp, color):
        asm.add(wp, name=name, color=cq.Color(color))
        solids[name] = wp

    add("lower_deck", parts["01_lower_deck"][0].translate((0, 0, z_low)), "steelblue")
    add("upper_deck", parts["02_upper_deck"][0].translate((0, 0, z_up)), "steelblue")
    for i, (cx, cy) in enumerate(column_pts()):
        add(f"column_{i}", column(P.COLUMN_DEFAULT).translate((cx, cy, z_col)), "gray")
    add("battery_tray", parts["04_battery_tray"][0].translate((0, 0, z_up_top)), "teal")
    pin_x, pin_y, _, _ = tray_dims()
    batt = (cq.Workplane("XY").box(P.BATT_W, P.BATT_L, P.BATT_H, centered=(True, True, False))
            .translate((0, -pin_y + P.BATT_L / 2 + 0.5, z_up_top + P.TRAY_BASE_T)))
    add("battery", batt, "blue")
    for b, (deck, xy, rot) in P.PLACEMENT.items():
        zt = z_col if deck == "lower" else z_up_top
        add(f"carrier_{b}", place(carrier(b), xy, zt, rot), "orange")
        zb = zt + P.CARRIER_T + P.BOARDS[b]["standoff_h"]
        add(f"board_{b}", place(board_standin(b), xy, zb, rot), "green")
    sx, sy = P.SWITCH_XY
    sw = (cq.Workplane("XY").circle(11.5).extrude(3).translate((sx, sy, z_up_top))
          .union(cq.Workplane("XY").circle(9.0).extrude(20).translate((sx, sy, z_up_top - P.SWITCH_SKIN - 20))))
    add("switch", sw, "black")
    for i, (fx, fy) in enumerate([(sx * P.FOOT_X, sy * P.FOOT_Y) for sx in (-1, 1) for sy in (-1, 1)]):
        add(f"skid_foot_{i}", skid_foot().translate((fx, fy, z_low)), "orange")
    for name, wp, color in standins(z_low, z_up):
        add(name, wp, color)
    asm.save(os.path.join(out, "R1_assembly.step"))

    meta = dict(z_lower_deck_underside=z_low, z_upper_deck_top=z_up_top,
                foot_length_below_deck=round(foot_length(), 1),
                track_width_wheel_centres=round(2 * (P.DECK_W / 2 + P.WHEEL_GAP + P.WHEEL_W / 2), 1),
                overall_width=round(P.DECK_W + 2 * (P.WHEEL_GAP + P.WHEEL_W), 1),
                grid_holes_lower=len(grid_points(lower_excluded)),
                grid_holes_upper=len(grid_points(upper_excluded)))
    with open(os.path.join(out, "parts_summary.json"), "w") as f:
        json.dump(dict(parts=summary, assembly=meta), f, indent=2)
    return solids, summary, meta


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "out"
    _, summary, meta = main(out)
    print(json.dumps(dict(parts=summary, assembly=meta), indent=1))
