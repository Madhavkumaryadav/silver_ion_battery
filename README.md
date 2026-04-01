# Silver-Ion Battery Simulation (MATLAB and Python)

## 1. Overview

This project provides a practical, physics-inspired silver-ion battery simulation in both:

- Python: `python/silver_ion_battery_sim.py`
- MATLAB: `matlab/silver_ion_battery_sim.m`

The model is useful for:

- State of charge (SOC) tracking
- Terminal voltage prediction under charge/discharge current
- Dynamic polarization behavior

## 2. Model Concept

The battery is represented by an Equivalent Circuit Model (ECM) with:

- Open-circuit voltage: `OCV(SOC)`
- Series resistance: `R0`
- Polarization branch: `R1 || C1`

States:

- `soc` in `[0, 1]`
- `vp` polarization voltage

Sign convention:

- `I > 0`: discharge
- `I < 0`: charge

## 3. Governing Equations

SOC dynamics:

`dsoc/dt = -(eta * I) / Q_As`, where `Q_As = Q_Ah * 3600`

Polarization dynamics:

`dvp/dt = -(vp / (R1 * C1)) + (I / C1)`

Terminal voltage:

`Vt = OCV(soc) - I * R0 - vp`

## 4. Default Parameters

- `Q_Ah = 2.0`
- `R0 = 0.035 Ohm`
- `R1 = 0.020 Ohm`
- `C1 = 2200.0 F`
- `eta_charge = 0.995`
- `eta_discharge = 1.0`
- `V_min = 2.8 V`
- `V_max = 4.2 V`

These are engineering starter values for workflow demonstration.

## 5. Current Profile

- `0-600 s`: rest (`I = 0.0 A`)
- `600-4200 s`: discharge (`I = +1.0 A`)
- `4200-4800 s`: rest (`I = 0.0 A`)
- `4800-7800 s`: charge (`I = -0.8 A`)
- `7800-9000 s`: rest (`I = 0.0 A`)

## 6. Project Structure

```text
silver_ion_battery/
	README.md
	requirements.txt
	results.csv
	docs/
		silver-ion-battery-making-guide.md
	python/
		silver_ion_battery_sim.py
	matlab/
		silver_ion_battery_sim.m
```

## 7. Python Usage

From project root:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python python/silver_ion_battery_sim.py
```

Optional CSV output:

```bash
python python/silver_ion_battery_sim.py --csv results.csv
```

Headless run:

```bash
python python/silver_ion_battery_sim.py --no-plot --csv results.csv
```

## 8. MATLAB Usage

From MATLAB:

```matlab
run('matlab/silver_ion_battery_sim.m')
```

## 9. Documentation for Making Process

The full step-by-step educational documentation for silver-ion battery making, including chemical roles, approximate quantity ranges, and architecture diagram is available in:

- `docs/silver-ion-battery-making-guide.md`

## 10. Disclaimer

This project is for educational and engineering prototyping use. For physical battery development, use verified chemistry data, proper safety controls, and expert supervision.
