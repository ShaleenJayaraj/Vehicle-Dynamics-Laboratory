"""R1 parameters for the self-balancing robot chassis. All units mm.

Frame: X = axle direction (wheels at +/-X), Y = fore-aft (fall direction), Z = up.
Origin = deck centre. Edit values here, then run build_r1.py to regenerate.

Values tagged MEASURED came from the owner (ruler). PROVISIONAL = estimate,
check against the real part before printing that part.
"""

# ---- printer / fit (update from test-coupon results) --------------------
M3_CLEAR = 3.4          # M3 clearance hole            (coupon -> pick best)
M3_PILOT = 2.5          # M3 self-tapping pilot hole   (coupon -> pick best)
SWITCH_HOLE = 20.0      # round rocker panel hole      (coupon -> 19.5/20.0/20.5)

# ---- decks ---------------------------------------------------------------
DECK_W = 174.0          # along X
DECK_D = 140.0          # along Y (R0 was 125; deepened to fit boards)
LOWER_T = 5.0
UPPER_T = 5.0
CORNER_R = 6.0

GRID_PITCH = 10.0       # M3 grid on both decks
GRID_X_MAX = 70.0
GRID_Y_MAX = 60.0

COLUMN_XY = (77.0, 60.0)    # column centres at (+/-x, +/-y)
COLUMN_D = 12.0
COLUMN_LENGTHS = (60.0, 80.0, 100.0)   # print the set; 80 = default build
COLUMN_DEFAULT = 80.0

# ---- motor / bracket (MEASURED) -----------------------------------------
BRACKET_HOLES_X = 14.0      # along motor axis, centre-centre
BRACKET_HOLES_Y = 15.5      # across, centre-centre
BRACKET_SLOT_X = (58.0, 84.0)   # slot centre-line range along X (adjustable track)
MOTOR_D = 25.0
MOTOR_LEN = 51.0            # bracket face to end of encoder connector
AXLE_BELOW_DECK = 22.5      # flange to motor gap ~10 + radius 12.5 (CONFIRM)
WHEEL_D = 65.0
WHEEL_W = 22.0
WHEEL_GAP = 10.0            # bracket face to wheel inner face
BRACKET_WALL = 2.5          # PROVISIONAL bracket plate thickness

MOTOR_WIRE_SLOT = dict(x=35.0, w=10.0, l=24.0)   # pass-throughs for encoder cables

# ---- upper deck features ----------------------------------------------
SWITCH_XY = (-50.0, 0.0)
SWITCH_SKIN = 2.0           # panel thickness the switch clips onto
SWITCH_POCKET_D = 32.0      # counterbore from underside
UPPER_SLOTS = [(-50.0, 61.0), (50.0, 61.0), (-50.0, -61.0), (50.0, -61.0)]
UPPER_SLOT_L, UPPER_SLOT_W = 40.0, 8.0

# ---- battery (MEASURED: Zeee 3S 2200, body only) --------------------------
BATT_L, BATT_W, BATT_H = 70.0, 28.0, 25.0
BATT_CLEAR = 1.5            # per side
TRAY_BASE_T = 4.0
TRAY_WALL_T = 3.0
TRAY_WALL_H = 15.0
TRAY_EAR_Y = 50.0           # tray mount holes at (+/-10, +/-TRAY_EAR_Y)
STRAP_GROOVE_W = 22.0
STRAP_GROOVE_DEPTH = 2.0
STRAP_GROOVE_Y = 18.0

# ---- boards: outline (w along X, h along Y), holes about board centre --------
STANDOFF_D = 7.0
STANDOFF_H = 6.0
CARRIER_T = 3.0
CARRIER_MARGIN = 2.0     # carrier outline beyond board edge
BOARDS = {
    # Arduino UNO R3 reference outline/holes (standard; Elegoo clone matches)
    "uno": dict(w=68.6, h=53.3, hole_d=3.2, status="STANDARD",
                holes=[(13.97 - 34.3, 2.54 - 26.65), (15.24 - 34.3, 50.80 - 26.65),
                       (66.04 - 34.3, 7.62 - 26.65), (66.04 - 34.3, 35.56 - 26.65)],
                mounts=[(-40, -10), (-40, 10), (40, -10), (40, 10)], standoff_h=6.0),
    "xy160d": dict(w=52.0, h=52.0, hole_d=3.2, status="PROVISIONAL",
                   holes=[(-22.5, -22.5), (-22.5, 22.5), (22.5, -22.5), (22.5, 22.5)],
                   mounts=[(-40, -10), (-40, 10), (40, -10), (40, 10)], standoff_h=6.0),
    "zx052": dict(w=66.0, h=36.0, hole_d=3.0, status="PROVISIONAL",
                  holes=[(-30.5, -15), (-30.5, 15), (30.5, -15), (30.5, 15)],
                  mounts=[(-40, -10), (-40, 10), (40, -10), (40, 10)], standoff_h=6.0),
    "gy521": dict(w=21.0, h=16.0, hole_d=3.0, status="PROVISIONAL",
                  holes=[(-7.7, 5.5), (7.7, 5.5)],
                  support=[(0.0, -5.0)],   # pin-free post under header end
                  mounts=[(-20, 0), (20, 0)], standoff_h=4.0),
}
# placement: deck, centre (x, y), rotation deg about Z
PLACEMENT = {
    "xy160d": ("lower", (0.0, 40.0), 0.0),
    "zx052":  ("lower", (0.0, -40.0), 0.0),
    "gy521":  ("lower", (0.0, 0.0), 0.0),
    "uno":    ("upper", (50.0, 0.0), 90.0),
}

# ---- skid feet / rest stand ------------------------------------------------
FOOT_X = 55.0               # 4 feet under lower deck at (+/-FOOT_X, +/-FOOT_Y)
FOOT_Y = 60.0
FOOT_HOLE_DX = 5.0          # foot screws at (FOOT_X +/- 5, FOOT_Y): clear of carriers
REST_ANGLE_DEG = 20.0       # robot rests at this tilt on the feet
FOOT_W, FOOT_T = 16.0, 10.0
