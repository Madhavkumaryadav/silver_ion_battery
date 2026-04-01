# Silver-Ion Battery Simulation Documentation (MATLAB and Python)

## 1. Overview

This project provides a practical, physics-inspired silver-ion battery simulation in both:

- Python: `python/silver_ion_battery_sim.py`
- MATLAB: `matlab/silver_ion_battery_sim.m`

The goal is to give you a consistent reference model for:

- State of charge (SOC) evolution over time
- Terminal voltage response under charge/discharge current
- Dynamic polarization effects (first-order RC branch)

This is a reduced-order engineering model suitable for algorithm development, controller prototyping, and workflow validation.

## 2. Model Scope and Assumptions

The model is an Equivalent Circuit Model (ECM) with:

- Open-circuit voltage `OCV(SOC)`
- Series ohmic resistance `R0`
- One polarization branch: `R1 || C1`

Assumptions:

- Cell temperature is constant
- Capacity fade and resistance growth are not time-varying in this baseline version
- OCV is an analytic function of SOC (can later be replaced by lookup table data)
- Coulombic efficiency is represented by a constant term during charging

## 3. Mathematical Formulation

### 3.1 States

- `soc` in `[0, 1]`
- `vp` polarization voltage across RC branch

### 3.2 Inputs

- Current `I` (A), sign convention in this project:
  - `I > 0`: discharge
  - `I < 0`: charge

### 3.3 Dynamics

1. SOC dynamics:

```
(dsoc/dt) = -(eta * I) / (Q_As)
```

where:

- `Q_As = Q_Ah * 3600`
- `eta = eta_discharge` if `I >= 0`, otherwise `eta_charge`

2. Polarization branch:

```
(dvp/dt) = -(1 / (R1 * C1)) * vp + (1 / C1) * I
```

### 3.4 Terminal voltage

```
Vt = OCV(soc) - I * R0 - vp
```

### 3.5 OCV function (default)

The baseline smooth approximation is:

```
OCV(soc) = a0 + a1*soc + a2*soc^2 + a3*log(soc + eps) + a4*log(1 - soc + eps)
```

with clipping to avoid singular logs near 0 and 1.

## 4. Default Parameters

Baseline parameters included in both implementations:

- Nominal capacity `Q_Ah = 2.0`
- Ohmic resistance `R0 = 0.035` Ohm
- Polarization resistance `R1 = 0.020` Ohm
- Polarization capacitance `C1 = 2200.0` F
- Charge efficiency `eta_charge = 0.995`
- Discharge efficiency `eta_discharge = 1.0`
- Voltage limits for reference:
  - `V_min = 2.8` V
  - `V_max = 4.2` V
- Initial conditions:
  - `soc0 = 0.95`
  - `vp0 = 0.0`

Note: these are example engineering values for workflow demonstration, not a validated chemistry dataset.

## 5. Current Profile

A piecewise profile is used in both implementations:

- `0 - 600 s`: rest (`I = 0.0 A`)
- `600 - 4200 s`: discharge (`I = +1.0 A`)
- `4200 - 4800 s`: rest (`I = 0.0 A`)
- `4800 - 7800 s`: charge (`I = -0.8 A`)
- `7800 - 9000 s`: rest (`I = 0.0 A`)

You can modify this profile directly in code or replace it with a file-driven current trace.

## 6. Project Structure

```
silver_ion_battery/
  README.md
  requirements.txt
  python/
    silver_ion_battery_sim.py
  matlab/
    silver_ion_battery_sim.m
```

## 7. Python Usage

### 7.1 Setup

From project root:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 7.2 Run simulation

```bash
python python/silver_ion_battery_sim.py
```

### 7.3 Optional output CSV

```bash
python python/silver_ion_battery_sim.py --csv results.csv
```

### 7.4 Disable plotting (headless run)

```bash
python python/silver_ion_battery_sim.py --no-plot --csv results.csv
```

## 8. MATLAB Usage

From MATLAB Command Window:

```matlab
run('matlab/silver_ion_battery_sim.m')
```

Outputs:

- Figures for current, SOC, polarization voltage, and terminal voltage
- Struct variable `sim_out` in workspace with fields:
  - `t_s`, `I_A`, `soc`, `vp_V`, `Vt_V`

## 9. Parameter Identification Workflow (Recommended)

To make this model chemistry-specific for your silver-ion cell:

1. OCV characterization:
- Run low-current charge/discharge or GITT test
- Build `OCV vs SOC` table
- Replace analytic `OCV(soc)` with interpolation from measured data

2. Dynamic branch fitting:
- Perform pulse current tests at multiple SOC levels
- Fit `R0`, `R1`, `C1` from voltage transients

3. Validation:
- Run independent drive cycles
- Compare predicted and measured voltage
- Compute RMSE and max absolute error

4. Optional improvements:
- Make `R0`, `R1`, `C1` functions of SOC and temperature
- Add second RC branch for better dynamic fidelity
- Add thermal submodel

## 10. Notes on Sign Conventions

This project uses:

- `I > 0`: discharge
- `I < 0`: charge

If your lab data uses the opposite sign, invert current before feeding the model.

## 11. Troubleshooting

1. Voltage out of range:
- Verify OCV parameters and SOC clipping
- Check current sign convention

2. SOC drifting outside [0, 1]:
- Confirm `Q_Ah` and timestep
- Ensure SOC clipping is active

3. Python plot not shown:
- Install matplotlib
- Use `--no-plot` for server/headless environments

## 12. Extension Ideas

- Add calendar/cycle aging model for capacity and resistance drift
- Add temperature dependence with `R(T)` and `OCV(SOC,T)`
- Integrate estimator (EKF/UKF) for online SOC and SOH
- Batch-run parameter sweeps for design-of-experiments

## 13. Disclaimer

This package is intended as an educational and engineering starter model. For safety-critical design, use experimentally validated parameters and full verification workflows.

## 14. Additional Documentation

For a structured educational guide on silver-ion battery making concepts, chemical roles, approximate quantity ranges, step-by-step workflow, and an architecture diagram, see:

- [docs/silver-ion-battery-making-guide.md](docs/silver-ion-battery-making-guide.md)
