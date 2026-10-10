# -*- coding: utf-8 -*-
"""
通用 XY 模板（吸收 Gerry 中文路径、ace 轴契约、本规范次刻度）。
  python plot_xy_template.py
只改下方 DATA / 标题 / 拟合区间。输出：图名.png/pdf/tif + .opju
"""
from __future__ import annotations
import os, sys, time, shutil, argparse
from pathlib import Path
import numpy as np

# ---------- 配置 ----------
X = np.array([1,2,3,4,5, 5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11,11.5,12,12.5,13,
              13.5,14,15,16,17,18], float)
Y = np.array([0.003,0.004,0.004,0.007,0.008,
              0.141,0.713,1.066,1.225,1.318,1.371,1.406,1.431,1.449,1.459,
              1.467,1.472,1.475,1.476,1.477,1.477,
              1.477,1.477,1.472,1.470,1.464,1.460], float)
X_NAME, X_UNIT = "t", "min"
Y_NAME, Y_UNIT = "ΔT", "K"
FIG = "Fig_main"
TITLE = "实验名称 图名"
SUB = "姓名：________   日期：________"
FIT_EARLY = (1, 5)
FIT_LATE = (13.5, 18)
MARK_T = 6.0          # None 关闭垂线
SHOW_EXTRAP = True
# --------------------------


def _ascii_tmp() -> Path:
    p = Path("C:/Temp/OriginCal")
    p.mkdir(parents=True, exist_ok=True)
    return p


def _export(gp, out: Path, tmp: Path) -> list[Path]:
    files = []
    for ext, typ in (("png", "png"), ("pdf", "pdf"), ("tif", "tif")):
        name = f"{FIG}.{ext}"
        tfile = tmp / name
        try:
            saved = gp.save_fig(str(tfile).replace("\\", "/"), type=typ, replace=True, width=1600)
        except Exception as e:
            print("save_fig", typ, e)
            continue
        if tfile.exists() and tfile.stat().st_size > 0:
            out.mkdir(parents=True, exist_ok=True)
            dst = out / name
            shutil.copy2(tfile, dst)
            print("export", dst, dst.stat().st_size)
            files.append(dst)
        else:
            print("export empty", typ, saved)
    return files


def _save_opju(op, out: Path, tmp: Path) -> Path | None:
    t = tmp / f"{FIG}.opju"
    if t.exists():
        t.unlink()
    try:
        op.save(str(t).replace("\\", "/"))
    except Exception as e:
        print("op.save", e)
        return None
    time.sleep(0.3)
    if t.exists() and t.stat().st_size > 2000:
        out.mkdir(parents=True, exist_ok=True)
        dst = out / f"{FIG}.opju"
        try:
            if dst.exists():
                dst.unlink()
            shutil.copy2(t, dst)
            print("opju", dst, dst.stat().st_size)
            return dst
        except PermissionError:
            stamp = time.strftime("%Y%m%d_%H%M%S")
            dst2 = out / f"{FIG}_{stamp}.opju"
            shutil.copy2(t, dst2)
            print("opju locked->", dst2)
            return dst2
    print("OPJU save failed — keep Origin open for Ctrl+S")
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path.cwd())
    ap.add_argument("--show", action="store_true", default=True)
    args = ap.parse_args()
    out = args.out.resolve()
    tmp = _ascii_tmp()

    try:
        os.system("taskkill /f /im Origin64.exe >nul 2>&1")
        time.sleep(1)
    except Exception:
        pass

    import originpro as op
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from apply_style import apply_lab_axes, apply_publication_axes, set_axis_titles, set_minor_ticks, apply_page_inches, reassert_axes_after_rescale

    op.set_show(args.show)
    op.new()

    # 数据：先落审计 CSV（utf-8-sig）
    out.mkdir(parents=True, exist_ok=True)
    audit = out / f"{FIG}_audit.csv"
    np.savetxt(audit, np.column_stack([X, Y]), delimiter=",", header=f"{X_NAME},{Y_NAME}", comments="", fmt="%.6g", encoding="utf-8-sig")

    wks = op.new_sheet()
    wks.cols = 6
    wks.from_list(0, X.tolist(), X_NAME, X_UNIT, axis="X")
    wks.from_list(1, Y.tolist(), Y_NAME, Y_UNIT, axis="Y")

    gp = op.new_graph(FIG, template="LINESYMB")
    gl = gp[0]
    p = gl.add_plot(wks, coly=1, colx=0, type="linesymbol")
    p.lname = "measured"
    p.color = 1
    p.lt_exec("line.width = 2; symbol.size = 5;")
    gl.rescale()

    note = SUB

    def _fit(lo, hi):
        m = (X >= lo) & (X <= hi)
        a, b = np.polyfit(X[m], Y[m], 1)
        return a, b
    if SHOW_EXTRAP and FIT_EARLY and FIT_LATE:
        a1, b1 = _fit(*FIT_EARLY)
        a2, b2 = _fit(*FIT_LATE)
        te = np.linspace(X.min() - 0.5, X.mean(), 20)
        wks.from_list(2, te.tolist(), "t_e", X_UNIT, axis="X")
        wks.from_list(3, (a1 * te + b1).tolist(), "y_e", Y_UNIT, axis="Y")
        pe = gl.add_plot(wks, coly=3, colx=2, type="line")
        pe.color = 2
        pe.lt_exec("line.style = 2; line.width = 2;")
        tl = np.linspace(X.mean(), X.max() + 0.5, 20)
        wks.from_list(4, tl.tolist(), "t_l", X_UNIT, axis="X")
        wks.from_list(5, (a2 * tl + b2).tolist(), "y_l", Y_UNIT, axis="Y")
        pl = gl.add_plot(wks, coly=5, colx=4, type="line")
        pl.color = 4
        pl.lt_exec("line.style = 2; line.width = 2;")

    y0, y1 = float(Y.min()) - 0.08, float(Y.max()) + 0.12
    if MARK_T is not None and FIT_EARLY and FIT_LATE:
        a1, b1 = _fit(*FIT_EARLY)
        a2, b2 = _fit(*FIT_LATE)
        T1, T2 = a1 * MARK_T + b1, a2 * MARK_T + b2
        dT = T2 - T1
        gl.add_line(MARK_T, y0, MARK_T, y1)
        gl.add_label(f"({MARK_T:.2f}, {T1:.3f})", x=MARK_T + 0.15, y=T1 - 0.08)
        gl.add_label(f"({MARK_T:.2f}, {T2:.3f})", x=MARK_T + 0.15, y=T2 + 0.03)
        gl.add_label(f"ΔT = {dT:.3f} {Y_UNIT}", x=MARK_T + 1.6, y=0.5 * (T1 + T2))
        note = f"ΔT = {dT:.3f} {Y_UNIT}   |   {SUB}"

    # 自动轴范围：数据 + 外推线 + 关键点，留余量后按 1/2/5 取整（避免裁切/手调）
    _xv = [float(X.min()), float(X.max())]
    pad_x = (X.max() - X.min()) * 0.08
    gl.set_xlim(X.min() - pad_x, X.max() + pad_x)

    _yvals = list(Y)
    try:
        _yvals += list(Y_e_vals) + list(Y_l_vals)
    except NameError:
        pass
    _ymin, _ymax = float(min(_yvals)), float(max(_yvals))
    _pad = max((_ymax - _ymin) * 0.08, 0.02)
    _ran = (_ymax + _pad) - (_ymin - _pad)
    _step = next(s for s in (0.05, 0.1, 0.2, 0.5, 1.0) if _ran / s <= 10)
    _y0 = float(np.floor((_ymin - _pad) / _step) * _step)
    _y1 = float(np.ceil((_ymax + _pad) / _step) * _step)
    gl.set_ylim(_y0, _y1)
    globals()["Y_AUTO_STEP"] = _step

    reassert_axes_after_rescale(gl, gp, publication=False)
    set_axis_titles(gl, f"{X_NAME} / {X_UNIT}", f"{Y_NAME} / {Y_UNIT}")
    set_minor_ticks(gp)
    apply_page_inches(gp, 16, 11)
    gp.activate()
    gp.lt_exec(f'label -s -sa -n title "{TITLE}";')
    gp.lt_exec(f'label -s -sa -n subtitle "{note}";')
    reassert_axes_after_rescale(gl, gp)  # 导出前再刷一次

    _export(gp, out, tmp)
    _save_opju(op, out, tmp)
    print("DONE", out)


if __name__ == "__main__":
    main()
