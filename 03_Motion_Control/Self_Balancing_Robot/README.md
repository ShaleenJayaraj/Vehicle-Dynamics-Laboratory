# Two-Wheel Self-Balancing Robot

Part of **Vehicle Dynamics Laboratory → Motion Control**.

A two-wheel inverted-pendulum robot, built to learn embedded motion control through a full model → predict → test → validate loop. The plant is derived and simulated in MATLAB/Simulink, PID and then LQR run on the hardware, and simulation is compared against measured behaviour with quantitative metrics (overshoot, settling time, steady-state error, noise, sample rate).

![R1 chassis](hardware/cad/R1/renders/R1_render.png)
*Chassis R1: parametric CadQuery model with stand-ins for the motors, boards and battery.*

## Status

| Phase | State |
|---|---|
| Component identification | ✅ All main parts identified and measured ([BOM](docs/BOM.md)) |
| Chassis CAD | ✅ R1 designed: [hardware/cad/R1](hardware/cad/R1/README.md) (3 board carriers waiting on hole measurements) |
| Printing & fit check | 🟡 Test coupons → decks, columns, tray, feet |
| Wiring & schematic | 🟡 Draft architecture and pin map ([docs/electrical.md](docs/electrical.md)) |
| Encoder characterization | ⬜ Counts per wheel revolution (hand-turn test) |
| Plant model & simulation | ⬜ |
| PID balance | ⬜ |
| LQR balance | ⬜ |
| Sim-vs-hardware validation | ⬜ |

## Hardware

| Function | Part | Key numbers |
|---|---|---|
| MCU | Elegoo UNO R3 (ATmega328P) | 16 MHz, 2 KB SRAM, interrupts on D2/D3 |
| IMU | MPU-6050 (GY-521) | I2C, mounted on the axle line |
| Motor driver | XY-160D dual H-bridge | ~6.5–27 V, ~7 A/ch (listing) |
| Logic supply | ZX-052 adjustable buck | 3S → 5 V / 7.5 V |
| Drive | 2× JGA25-371, 12 V, 130 RPM, Hall quadrature encoder | Ø65 × 22 mm wheels → ~0.44 m/s no-load |
| Battery | Zeee LiPo 3S 2200 mAh | 70 × 28 × 25 mm, 11.1 V nominal / 12.6 V max |
| Power | Inline ATO fuse (5 A), round rocker switch (6 A), T-plug | |

## Chassis R1 at a glance
- Two 174 × 140 × 5 mm decks on 4 columns (60/80/100 mm lengths, so CoM height can be a test variable).
- A 10 mm M3 grid on both decks. Each board sits on its own small carrier, so the layout can be reconfigured and the battery moved fore/aft to trim the CoM.
- Motors and brackets mount under the lower deck on slots (adjustable track width, 216 mm nominal).
- 4 skid feet stop a fall at 20° and double as a rest stand.
- Printed in ABS on a Bambu H2D.

## Control roadmap
1. **Model:** wheeled inverted-pendulum equations of motion, linearization about upright, open-loop poles; include motor saturation (~130 RPM).
2. **Estimation:** IMU pitch via a complementary filter, then a Kalman filter. Bias and noise characterization.
3. **PID:** pitch loop, then a cascaded wheel-velocity/position loop.
4. **System ID:** motor step tests, encoder scaling, model update with uncertainty.
5. **LQR:** full-state feedback on [x, ẋ, φ, φ̇]; compared with PID on identical disturbance tests.
6. **Stretch goals:** observer/LQG, MPC.

## Folder layout
```
Self_Balancing_Robot/
├── docs/                 BOM, electrical architecture, build log
├── hardware/
│   ├── cad/R1/           chassis R1: STEP, STL, parametric source, renders, test coupons
│   └── electronics/      schematic, wire table
├── firmware/             UNO firmware
├── modeling/             EOM derivation, linearization, controller design, simulation
├── data/                 logged test runs + analysis scripts
└── media/                photos, renders, videos
```
