# -*- coding: utf-8 -*-
"""6min 垂线法 / 雷诺等面积法求 ΔT。 python calc_dt.py data.csv"""
import sys
import numpy as np

def load(path):
    d = np.loadtxt(path, delimiter=",", skiprows=1)
    return d[:, 0], d[:, 1]

def methods(x, y, t0=6.0):
    amp = y.max() - y.min()
    early = y <= y.min() + 0.15 * amp
    imax = int(np.argmax(y))
    late = x >= (x[imax + 3] if imax + 3 < len(x) else x[-3])
    if early.sum() < 3:
        early = x <= x[3]
    if late.sum() < 3:
        late = x >= x[-3]
    a1, b1 = np.polyfit(x[early], y[early], 1)
    a2, b2 = np.polyfit(x[late], y[late], 1)
    Te, Tl = (lambda t: a1 * t + b1), (lambda t: a2 * t + b2)
    T1, T2 = float(Te(t0)), float(Tl(t0))
    dT6 = T2 - T1

    trapz = getattr(np, "trapezoid", None) or np.trapz
    td = np.linspace(x[early][-1], x[late][0], 2001)
    yd = np.interp(td, x, y)

    def areas(tm):
        ml, mr = td <= tm, td >= tm
        return (trapz(yd[ml] - Te(td[ml]), td[ml]),
                trapz(Tl(td[mr]) - yd[mr], td[mr]))

    grid = np.linspace(td[0] + 0.1, td[-1] - 0.1, 400)
    diff = np.array([areas(t)[0] - areas(t)[1] for t in grid])
    sc = np.where(np.diff(np.sign(diff)))[0]
    if len(sc):
        i = sc[0]
        tm = float(grid[i] + (grid[i + 1] - grid[i]) * (0 - diff[i]) / (diff[i + 1] - diff[i]))
    else:
        tm = float(grid[np.argmin(np.abs(diff))])
    T1r, T2r = float(Te(tm)), float(Tl(tm))
    SL, SR = areas(tm)
    return dict(a1=a1, b1=b1, a2=a2, b2=b2,
                T1_6=T1, T2_6=T2, dT_6=dT6, t0=t0,
                tm=tm, T1_r=T1r, T2_r=T2r, dT_r=T2r - T1r,
                S1=SL, S2=SR)

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "data.csv"
    x, y = load(path)
    r = methods(x, y)
    for k, v in r.items():
        print(f"{k}: {v:.6f}" if isinstance(v, float) else f"{k}: {v}")
    print(f"dT_A={r['dT_6']:.4f}  dT_B={r['dT_r']:.4f}  diff={r['dT_r']-r['dT_6']:.4f}")
