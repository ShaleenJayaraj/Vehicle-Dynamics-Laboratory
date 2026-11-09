# Build Log

Record each session with its date, goal, setup, measurements (with units and instrument), result and next step.

---

## Before 2026-11-09: component checks (moved over from earlier notes)
- Both motors turn smoothly by hand, with some gearbox resistance and no shaft wobble.
- Battery terminal reading: 11.47 V (probe points not recorded).
- Encoder powered from the UNO: LED on. UNO 5 V rail read about 4.7 V alone and about 4.3 V with the encoder attached. Probe points were not recorded, so this is not a characterized load test.
- Signal test on the encoder outputs is still pending.

## 2026-11-09: project setup
- Identified the parts from photos (see [BOM](BOM.md)).
- Drafted the power architecture and pin map ([electrical.md](electrical.md)).
- CAD R0 packaging concept done (assumed dimensions).
- **Next:** read the motor and battery labels; run the encoder count test.
