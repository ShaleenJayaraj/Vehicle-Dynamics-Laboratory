# Build Log

Record each session with its date, goal, setup, measurements (with units and instrument), result and next step.

---

## Before 2026-11-09: component checks (moved over from earlier notes)
- Both motors turn smoothly by hand, with some gearbox resistance and no shaft wobble.
- Battery terminal reading: 11.47 V (probe points not recorded).
- Encoder powered from the UNO: LED on. UNO 5 V rail read about 4.7 V alone and about 4.3 V with the encoder attached (probe points not recorded).

## 2026-11-09: project setup
- Identified the parts from photos; drafted the power architecture and pin map.
- Reviewed the ChatGPT CAD R0: no board mounts, and its motor slots and battery tray didn't match the real parts.

## 2026-11-12: measurements + CAD R1
- Labels read: motors **JGA25-371 12 V 130 RPM**; battery **Zeee 3S 2200 mAh**.
- Measured (ruler): battery 70 × 28 × 25 mm; bracket hole pattern 14 × 15.5 mm; motor 51 mm from bracket to end of connector; wheels Ø65 × 22 mm; switch bezel Ø23 (panel hole ~Ø20).
- iPhone Measure app checked against the UNO's known size: off by ~5 mm, so it's only used for rough packaging.
- Found that the supplied fuse is 20 A (yellow): to replace with 5 A.
- Generated test coupons (M3 and switch hole sizes) and chassis **R1** (parametric CadQuery, STEP/STL). The assembly interference check found no collisions.
- **Next:** print the coupons → decks, columns, tray, UNO carrier, feet; measure the remaining board hole patterns; encoder count test.
