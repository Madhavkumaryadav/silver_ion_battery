import argparse
import csv
from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np


@dataclass
class BatteryParams:
    q_ah: float = 2.0
    r0_ohm: float = 0.035
    r1_ohm: float = 0.020
    c1_f: float = 2200.0
    eta_charge: float = 0.995
    eta_discharge: float = 1.0
    v_min: float = 2.8
    v_max: float = 4.2


@dataclass
class SimConfig:
    t_end_s: float = 9000.0
    dt_s: float = 1.0
    soc0: float = 0.95
    vp0_v: float = 0.0


def current_profile_a(t_s: np.ndarray) -> np.ndarray:
    i = np.zeros_like(t_s)
    i[(t_s >= 600.0) & (t_s < 4200.0)] = 1.0
    i[(t_s >= 4800.0) & (t_s < 7800.0)] = -0.8
    return i


def ocv_from_soc(soc: np.ndarray) -> np.ndarray:
    eps = 1e-6
    s = np.clip(soc, eps, 1.0 - eps)

    a0 = 3.10
    a1 = 1.00
    a2 = -0.22
    a3 = 0.05
    a4 = -0.04

    return a0 + a1 * s + a2 * s * s + a3 * np.log(s) + a4 * np.log(1.0 - s)


def run_simulation(params: BatteryParams, cfg: SimConfig) -> dict:
    t_s = np.arange(0.0, cfg.t_end_s + cfg.dt_s, cfg.dt_s)
    n = t_s.size

    i_a = current_profile_a(t_s)

    soc = np.zeros(n)
    vp_v = np.zeros(n)
    vt_v = np.zeros(n)

    soc[0] = np.clip(cfg.soc0, 0.0, 1.0)
    vp_v[0] = cfg.vp0_v

    q_as = params.q_ah * 3600.0

    for k in range(n - 1):
        ik = i_a[k]
        eta = params.eta_discharge if ik >= 0.0 else params.eta_charge

        dsoc_dt = -(eta * ik) / q_as
        dvp_dt = -(vp_v[k] / (params.r1_ohm * params.c1_f)) + (ik / params.c1_f)

        soc[k + 1] = np.clip(soc[k] + cfg.dt_s * dsoc_dt, 0.0, 1.0)
        vp_v[k + 1] = vp_v[k] + cfg.dt_s * dvp_dt

    ocv_v = ocv_from_soc(soc)
    vt_v = ocv_v - i_a * params.r0_ohm - vp_v

    return {
        "t_s": t_s,
        "i_a": i_a,
        "soc": soc,
        "vp_v": vp_v,
        "ocv_v": ocv_v,
        "vt_v": vt_v,
    }


def write_csv(path: str, data: dict) -> None:
    keys = ["t_s", "i_a", "soc", "vp_v", "ocv_v", "vt_v"]
    rows = zip(*(data[k] for k in keys))

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(keys)
        writer.writerows(rows)


def plot_results(data: dict, params: BatteryParams) -> None:
    t = data["t_s"]

    fig, axes = plt.subplots(4, 1, figsize=(10, 10), sharex=True)

    axes[0].plot(t, data["i_a"], linewidth=1.6)
    axes[0].set_ylabel("Current (A)")
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(t, data["soc"], linewidth=1.6)
    axes[1].set_ylabel("SOC")
    axes[1].set_ylim(-0.02, 1.02)
    axes[1].grid(True, alpha=0.3)

    axes[2].plot(t, data["vp_v"], linewidth=1.6)
    axes[2].set_ylabel("V_p (V)")
    axes[2].grid(True, alpha=0.3)

    axes[3].plot(t, data["vt_v"], label="Terminal voltage", linewidth=1.8)
    axes[3].axhline(params.v_min, linestyle="--", linewidth=1.0, label="V_min")
    axes[3].axhline(params.v_max, linestyle="--", linewidth=1.0, label="V_max")
    axes[3].set_ylabel("Voltage (V)")
    axes[3].set_xlabel("Time (s)")
    axes[3].grid(True, alpha=0.3)
    axes[3].legend(loc="best")

    fig.suptitle("Silver-Ion Battery ECM Simulation")
    fig.tight_layout()
    plt.show()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Silver-ion battery ECM simulation")
    parser.add_argument("--csv", type=str, default="", help="Optional CSV output path")
    parser.add_argument("--no-plot", action="store_true", help="Disable plotting")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    params = BatteryParams()
    cfg = SimConfig()

    data = run_simulation(params, cfg)

    if args.csv:
        write_csv(args.csv, data)
        print(f"Saved simulation data to: {args.csv}")

    print("Simulation complete")
    print(f"Final SOC: {data['soc'][-1]:.4f}")
    print(f"Final terminal voltage: {data['vt_v'][-1]:.4f} V")

    if not args.no_plot:
        plot_results(data, params)


if __name__ == "__main__":
    main()
