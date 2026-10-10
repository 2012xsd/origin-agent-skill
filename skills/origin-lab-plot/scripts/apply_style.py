# -*- coding: utf-8 -*-
"""轴契约 / 出版样式 / 次刻度 — 供 plot 模板与手写脚本 import。"""
from __future__ import annotations

# 实验课：底/左可见，线宽 2，变量+量纲
LAB_AXES_LT = """
layer.x.show=1; layer.y.show=1;
layer.x.showAxes=1; layer.y.showAxes=1;
layer.x.showLabels=1; layer.y.showLabels=1;
layer.x.showopposite=0; layer.y.showopposite=0;
layer.x.opposite=0; layer.y.opposite=0;
layer.x.color=color(0,0,0); layer.y.color=color(0,0,0);
layer.x.thickness=2; layer.y.thickness=2;
layer.x.ticks=1; layer.y.ticks=1;
layer.x.ticklength=8; layer.y.ticklength=8;
layer.x.grid.show=0; layer.y.grid.show=0;
"""

# 论文四边框：顶/右有框无刻度无标签
PUB_FRAME_LT = """
layer.x.showAxes=3; layer.y.showAxes=3;
layer.x.showLabels=1; layer.y.showLabels=1;
layer.x2.showlabel=0; layer.y2.showlabel=0;
layer.x2.ticks=0; layer.y2.ticks=0;
layer.x.thickness=2; layer.y.thickness=2;
layer.x2.thickness=2; layer.y2.thickness=2;
layer.tickW=2.0; layer.tickstyle=1;
layer.x.grid.show=0; layer.y.grid.show=0;
"""


def apply_lab_axes(gl, *, thickness: float = 2.0) -> None:
    """普通实验图：底 x + 左 y 必须可见（轴契约）。"""
    gl.lt_exec(LAB_AXES_LT.replace("2;", f"{thickness};").replace("thickness=2\n", f"thickness={thickness}\n"))
    # 上面 replace 可能过度，直接再刷一遍带厚度
    gl.lt_exec(f"layer.x.thickness={thickness}; layer.y.thickness={thickness};")


def apply_publication_axes(gl, *, thickness: float = 2.0) -> bool:
    """四边框出版样式；顶/右无刻度标签。"""
    gl.lt_exec(PUB_FRAME_LT)
    gl.lt_exec(f"layer.x.thickness={thickness}; layer.y.thickness={thickness}; layer.x2.thickness={thickness}; layer.y2.thickness={thickness};")
    return True


def set_axis_titles(gl_or_gp, x_title: str, y_title: str) -> None:
    """轴标题：变量名称 + 量纲。"""
    # 优先 layer 内 axis API，退回 LabTalk
    try:
        gl_or_gp.axis("x").title = x_title
        gl_or_gp.axis("y").title = y_title
    except Exception:
        obj = gl_or_gp
        obj.lt_exec(f'xb.text$ = "{x_title}";')
        obj.lt_exec(f'yl.text$ = "{y_title}";')


def set_minor_ticks(gp, *, n_x: int = 4, n_y: int = 4, label: bool = True) -> None:
    """规范第9条：次刻度要标注。n_* = 每主刻度间隔数。"""
    gp.lt_exec(f"layer.x.minor = {n_x}; layer.y.minor = {n_y};")
    gp.lt_exec("layer.x.minorsize = 4; layer.y.minorsize = 4;")
    if label:
        try:
            gp.lt_exec("layer.x.minorlabel = 1; layer.y.minorlabel = 1;")
            gp.lt_exec("layer.x.minorlabelsize = 10; layer.y.minorlabelsize = 10;")
        except Exception:
            pass


def apply_page_inches(gp, w_cm: float = 16.0, h_cm: float = 11.0) -> None:
    gp.set_float("page.width", w_cm / 2.54)
    gp.set_float("page.height", h_cm / 2.54)


def style_series(p, *, color=1, width: float = 2.0, symbol: int | None = None, dashed: bool = False) -> None:
    p.color = color
    if dashed:
        p.lt_exec(f"line.style = 2; line.width = {width};")
    elif symbol is None:
        p.lt_exec(f"line.width = {width};")
    else:
        p.lt_exec(f"line.width = {width}; symbol.size = {symbol};")


def reassert_axes_after_rescale(gl, gp, *, publication: bool = False) -> None:
    """rescale / legend / 分组后必须重刷（ace 规则）。"""
    if publication:
        apply_publication_axes(gl)
    else:
        apply_lab_axes(gl)
    try:
        set_minor_ticks(gp)
    except Exception:
        pass
