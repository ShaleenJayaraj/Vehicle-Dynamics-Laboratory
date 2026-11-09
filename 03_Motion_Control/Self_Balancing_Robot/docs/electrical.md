# Electrical Architecture (DRAFT, not built or verified)

## Power

```
3S LiPo ──T-plug── fuse ── switch ──┬── XY-160D motor supply (≤12.6 V)
                                    └── ZX-052 buck ──→ logic rail
All grounds common: battery −, driver GND, buck −, UNO GND, IMU GND
```

Logic rail options:
- **Buck at ~7.5 V → UNO VIN** (recommended). The UNO's regulator stays in the path, so plugging in USB at the same time is safe.
- **Buck at 5.0 V → UNO 5V pin.** This bypasses the regulator. Don't power from USB and the buck at the same time.

If the motors are 6 V-rated, cap the PWM duty in firmware.

Battery sense: a 10 kΩ / 4.7 kΩ divider to A0 (12.6 V → ~4.03 V).

## Proposed UNO pin map

| Function | Pin | Reason |
|---|---|---|
| Left encoder A | D2 | INT0 |
| Right encoder A | D3 | INT1 |
| Left encoder B | D4 | read inside the ISR for direction |
| Right encoder B | D7 | read inside the ISR for direction |
| ENA (left PWM) | D9 | Timer1, PWM frequency can be changed without affecting millis() |
| ENB (right PWM) | D10 | Timer1 |
| IN1 / IN2 (left dir) | D5 / D6 | |
| IN3 / IN4 (right dir) | D8 / D11 | |
| IMU SDA / SCL | A4 / A5 | I2C |
| IMU INT (optional) | D12 (pin-change) | |
| Battery sense | A0 | divider |

This gives 2× quadrature decoding (A edges, B for direction). If encoder PPR × gear ratio turns out to be low, pin-change interrupts can provide full 4×.

## Before first power-up
- [ ] Confirm battery cell count on the balance lead
- [ ] Fuse rating chosen against motor stall current
- [ ] Buck output set and measured with no load connected
- [ ] Continuity and polarity check with power disconnected
- [ ] Motor wire colours mapped from the motor label or listing
