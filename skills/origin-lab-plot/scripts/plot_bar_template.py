# -*- coding: utf-8 -*-
"""柱状/分组柱模板。改 LABELS/SERIES 后运行。"""
from __future__ import annotations
import os, sys, time, shutil, argparse
from pathlib import Path
import numpy as np

LABELS = ["G1", "G2", "G3", "G4"]
SERIES = {
    "SeriesA": [10.2, 12.1, 9.8, 11.5],
    "SeriesB": [8.1, 9.4, 10.2, 8.9],
}
X_NAME, Y_NAME = "Group", "Value"
FIG = "Fig_bar"
TITLE = "实验名称 分组柱状图"
SUB = "姓名：________   日期：________"
COLORS = ["#4E6E8E", "#D9903D", "#2F8F83", "#8E4E6E"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path.cwd())
    args = ap.parse_args()
    out = args.out.resolve()
    tmp = Path("C:/Temp/OriginCal")
    tmp.mkdir(parents=True, exist_ok=True)

    os.system("taskkill /f /im Origin64.exe >nul 2>&1")
    time.sleep(1)

    import originpro as op
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from apply_style import apply_lab_axes, apply_publication_axes, set_axis_titles, set_minor_ticks, apply_page_inches

    op.set_show(True)
    op.new()

    out.mkdir(parents=True, exist_ok=True)
    cols = [LABELS] + [SERIES[k] for k in SERIES]
    wks = op.new_sheet()
    wks.cols = 1 + len(SERIES)
    wks.from_list(0, LABELS, X_NAME, "", axis="X")
    for i, k in enumerate(SERIES):
        wks.from_list(1 + i, SERIES[k], k, "", axis="Y")

    gp = op.new_graph(FIG, template="COLUMN")
    gl = gp[0]
    for i in range(len(SERIES)):
        p = gl.add_plot(wks, coly=1 + i, colx=0, type="c")
        p.lname = list(SERIES.keys())[i]
        p.color = COLORS[i % len(COLORS)]
    gl.rescale()
    apply_publication_axes(gl)
    apply_lab_axes(gl)
    set_axis_titles(gl, X_NAME, Y_NAME)
    set_minor_ticks(gp)
    apply_page_inches(gp, 16, 11)
    gp.activate()
    gp.lt_exec(f'label -s -sa -n title "{TITLE}";')
    gp.lt_exec(f'label -s -sa -n subtitle "{SUB}";')
    gp.lt_exec("legend -r;")

    for ext, typ in (("png", "png"), ("pdf", "pdf")):
        tfile = tmp / f"{FIG}.{ext}"
        try:
            gp.save_fig(str(tfile).replace("\\", "/"), type=typ, replace=True, width=1600)
            if tfile.exists() and tfile.stat().st_size:
                shutil.copy2(tfile, out / f"{FIG}.{ext}")
                print("export", out / f"{FIG}.{ext}")
        except Exception as e:
            print("export", ext, e)
    t = tmp / f"{FIG}.opju"
    if t.exists():
        t.unlink()
    op.save(str(t).replace("\\", "/"))
    if t.exists() and t.stat().st_size > 2000:
        shutil.copy2(t, out / f"{FIG}.opju")
        print("opju", out / f"{FIG}.opju")
    print("DONE")


if __name__ == "__main__":
    main()
