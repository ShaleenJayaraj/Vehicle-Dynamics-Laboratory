# Bill of Materials

Identified from component photos on 2026-11-09. Specs marked *(verify)* are typical listing values for that module, not confirmed against a datasheet or label.

| # | Item | Qty | Identified as | Key specs | To confirm | Photo |
|---|---|---|---|---|---|---|
| 1 | Microcontroller | 1 | Elegoo UNO R3 (ATmega328P) | 16 MHz, 5 V logic, 2 KB SRAM. Ext. interrupts D2/D3. PWM on D3, D5, D6, D9, D10, D11. I2C on A4/A5 | — | [photo](../media/elegoo_uno_r3.jpg) |
| 2 | IMU | 1 | GY-521, MPU-6050 | 3-axis gyro + accel, I2C 0x68 (0x69 with AD0 high), onboard 3.3 V LDO (VCC 5 V OK) | Mount orientation | [photo](../media/imu_mpu6050.jpg) |
| 3 | Motor driver | 1 | XY-160D dual H-bridge | ~6.5–27 V, ~7 A/ch *(verify)*. IN1–IN4, ENA/ENB | Seller pinout, max PWM frequency | [photo](../media/buck_zx052_driver_xy160d.jpg) |
| 4 | Buck converter | 1 | ZX-052 V2.0 with voltmeter display | LM2596-class *(verify)* | Set output before connecting loads | [photo](../media/buck_zx052_driver_xy160d.jpg) |
| 5 | Geared DC motor + encoder | 2 | 25 mm geared motor, rear Hall quadrature encoder, 6-wire lead (JGA25-370 style) | — | Rated V, gear ratio, encoder PPR, wire colours | [photo](../media/motor_encoder_wheel.jpg) |
| 6 | Motor bracket | 2 | L-bracket | — | Hole pattern | [photo](../media/motor_encoder_wheel.jpg) |
| 7 | Wheel | 2 | Rubber tyre, blue hub, ~65 mm OD (estimate) | — | Measure OD, width | [photo](../media/motor_encoder_wheel.jpg) |
| 8 | Battery | 1 | LiPo, T-plug main lead + JST-XH balance lead | 11.47 V measured → consistent with 3S | Cell count, capacity, C rating | — |
| 9 | Fuse | 1 | Inline blade-fuse holder | — | Rating | — |
| 10 | Switch | 1 | — | — | Rating | — |
| 11 | T-plug connectors | — | Deans-style | — | — | — |

## Measurements to record

| Parameter | Value | Method |
|---|---|---|
| Wheel OD / effective radius | | calipers; loaded radius from rolling distance |
| Track width (wheel centre to centre) | | assembled |
| Axle height | | assembled, loaded |
| Encoder counts per wheel revolution | | hand-turn test, both directions |
| Mass: each motor+bracket, wheel, battery, each board, chassis | | scale (note resolution) |
| Body CoM height above axle | | CAD mass properties + balance test |
| Body pitch inertia | | CAD estimate; pendulum swing test |
