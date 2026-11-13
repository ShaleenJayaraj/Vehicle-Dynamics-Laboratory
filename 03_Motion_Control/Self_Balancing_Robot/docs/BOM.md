# Bill of Materials

Updated 2026-11-12. Measurements were taken with a ruler unless noted. *(verify)* = typical listing value for that module, not confirmed against a datasheet.

## Electronics & drive

| # | Item | Qty | Part | Key specs | Open items |
|---|---|---|---|---|---|
| 1 | Microcontroller | 1 | Elegoo UNO R3 (ATmega328P) | 16 MHz, 5 V logic, 2 KB SRAM. Interrupts D2/D3; PWM D3/5/6/9/10/11; I2C A4/A5. Board 68.6 × 53.3, holes Ø3.2 (standard pattern) | — |
| 2 | IMU | 1 | GY-521, MPU-6050 | I2C 0x68, onboard 3.3 V LDO (VCC 5 V OK) | Hole spacing |
| 3 | Motor driver | 1 | XY-160D dual H-bridge | ~6.5–27 V, ~7 A/ch *(verify)*; IN1–IN4, ENA/ENB | Hole spacing, pinout, max PWM freq |
| 4 | Buck converter | 1 | ZX-052 V2.0 with voltmeter | LM2596-class *(verify)* | Hole spacing; set output before connecting |
| 5 | Gear motor + encoder | 2 | **JGA25-371, DC 12 V, 130 RPM** (SKU GS20179-04) | Ø25 mm; 6-wire JST lead (red, black, yellow, green, blue, white); 51 mm from bracket to end of connector | Gear ratio, encoder PPR, stall current, wire functions |
| 6 | Motor bracket | 2 | L-bracket, flange 30 × 24 mm | 4× Ø4 holes, **14 mm (along axis) × 15.5 mm (across)**; centre hole Ø10 | Flange-to-shaft-centre distance (assumed 22.5 mm) |
| 7 | Wheel | 2 | Rubber tyre, blue hub | **Ø65 × 22 mm**; inner face 10 mm from bracket | Effective rolling radius |
| 8 | Battery | 1 | **Zeee LiPo 3S 2200 mAh** | Body 70 × 28 × 25 mm; T-plug + JST-XH balance lead; 12.6 V max, ~9.9 V cutoff | C rating |
| 9 | Fuse | 1 | Inline holder, standard ATO blade | **Use 5 A** (the supplied 20 A yellow fuse is too high) | Review against stall current |
| 10 | Power switch | 1 | Round snap-in rocker (KCD1 type) | Bezel Ø23, body ~20 mm deep, 2 pins @ 7 mm, 6 A 125/250 VAC; panel hole ~Ø20 | Exact hole from test coupon |
| 11 | T-plug connectors | — | Deans-style | — | — |

## Printed parts (chassis R1, ABS)
See [hardware/cad/R1/README.md](../hardware/cad/R1/README.md) for files, quantities and print settings.

## Fasteners (M3 assortment)
34 × M3×12, 8 × M3×10, 14 × M3×8, 26 nuts, 8 washers. The breakdown is in the R1 README.

## Measurements still to record

| Parameter | Value | Method |
|---|---|---|
| XY-160D / ZX-052 / GY-521 hole spacing | | edge to edge minus hole Ø |
| Bracket flange-to-shaft-centre distance | | ruler / calipers |
| Encoder counts per wheel revolution | | hand-turn test, both directions |
| Mass of each component | | kitchen scale |
| Body CoM height above axle | | CAD + balance test |
| Body pitch inertia | | CAD estimate; pendulum swing test |
