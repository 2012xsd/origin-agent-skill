---
name: origin-lab-plot
icon: "📈"
description: Use when the user asks to plot scientific data in Origin/OriginPro or create/edit OPJU exports (Origin画图、originpro出图、温差图柱状图散点、导出OPJU/PNG/PDF、出版级Origin图). Local Windows Origin engine: originpro automation, axis contract, minor ticks, export QA. Experiment-specific graphing rules come from lab-graph-standards profiles — load that skill when the user names a lab or 作图规范. Any XY/bar dataset.
---

# origin-lab-plot（Origin 出图引擎）

职责：**怎么画** — 本机 Origin + originpro。  
**要什么图 / 按谁的规范** → 见配套 skill `lab-graph-standards`（按实验分类的规范库）。

## 何时用

- 「用 Origin 画图 / 出 OPJU / originpro 画散点柱状」
- 已有规范清单后要落地执行
- 配合 `lab-graph-standards` 使用

不用：matplotlib 当成品图（除非用户要）、网页图、纯算数。

## 与规范库分工

```
用户: 按××实验规范画图
  → lab-graph-standards  打开 standards/<experiment>.md，列清单
  → origin-lab-plot      金流程执行出图
  → present_files
```

新实验：只在规范库**新增** `standards/*.md`，不改本 skill。

## 环境（本机）

| 项 | 值 |
|---|---|
| Origin | 2026b · `D:\oirgin下载路径\Origin64.exe` |
| Python | `$env:MIMO_PYTHON` · `originpro` `pywin32` `numpy` `pandas` |
| COM | `Origin.Application`；启动前 `taskkill /f /im Origin64.exe` |

中文路径：先 `C:\Temp\OriginCal\`，再 `shutil.copy2`。

## 金流程（7 步）

1. **清场** kill → `op.set_show(True)` → `op.new()`
2. **读数**；审计 CSV `utf-8-sig`
3. **建表** `new_sheet` / `from_df`；X/Y designation
4. **建图** `add_plot(..., type='linesymbol'|'line'|'c'|'s'|'area')`（**小写**）
5. **刷轴** `apply_lab_axes` 或 `apply_publication_axes` → 次刻度 → 标题标注  
   （若有规范库清单，按清单补图上必标项）
6. **导出** ASCII 临时目录 `save_fig` + `save` → 拷回
7. **验收** PNG 非空、轴可见；`present_files`

`try/finally: op.exit()`。

## 轴契约（rescale/legend 后重刷）

```python
from apply_style import apply_lab_axes, apply_publication_axes, set_axis_titles, set_minor_ticks
apply_lab_axes(gl)   # 或 apply_publication_axes(gl)
set_axis_titles(gl, "t / min", "ΔT / K")
set_minor_ticks(gp)  # 若规范要求次刻度标注
```

普通 2D：底 x、左 y 轴线+主刻度+刻度值+轴标题。禁 line 假轴。

## 图型速查

| 图 | template | type |
|---|---|---|
| 点+线 | LINESYMB | linesymbol |
| 线 | LINE | line |
| 柱 | COLUMN | c |
| 散点 | SCATTER | s |
| 面积 | LINE | area |


## 必须保留的三条（两 skill 共有）

1. **附线性拟合结果表**（Origin 风格，前期/后期各一或标明段名）：
   方程 `y = a + b*x`；绘图；权重（如「不加权」）；
   **截距 a ± δa**、**斜率 b ± δb**、残差平方和、Pearson's r、
   R平方(COD)、调整后R平方。
   示例（前期）：截距 0.03553 ± 0.01989，斜率 0.04589 ± 0.01021，
   残差平方和 0.00183，r = 0.91358，R² = 0.83462，调整 R² = 0.79327。
   写入 `results.txt` 或图注/结果表。

2. **比例尺的选择**：
   ① 能表示测量值的测量精度；
   ② 每小格数值便于读数计算：一般取 **1、2、5** 或 **1、2、5 的 10ⁿ 倍**（n 整数），
      **不取**难读的 3、4、6、7、8、9 或其倍数；
   ③ 比例尺应使直线与横轴交角尽可能接近 **45°**。

3. **次刻度也要标注**：主、次刻度都画；次刻度按 1/2/5 细分；
   必要时刻度旁标数。LabTalk：`layer.x.minor = 4; layer.x.minorlabel = 1`。

## 硬性禁止

- 错误大小写 type/template；`new_book('名字')` 位置参数  
- `expGraph`、COM `save -i`  
- 编造误差棒；改用户单位/含义  
- matplotlib 冒充 Origin（除非用户同意降级）

## 按需文件

| 场景 | 路径 |
|---|---|
| 新写 XY/柱图 | `scripts/plot_xy_template.py` `plot_bar_template.py` |
| 样式/四边框/次刻度 | `scripts/apply_style.py` + `references/style-contracts.md` |
| API/报错 | `references/origin-api.md` `references/troubleshooting.md` |
| 验收 opju | `scripts/inspect_origin.py` |
| **实验规范** | **`lab-graph-standards` → `standards/<实验>.md`** |


## 交付时必给 Origin 源文件（.opju）

用户明确要求：**每次出图都附上可编辑的 `.opju` 源文件**，不能只给 PNG/PDF。

- 主交付列表里 **`.opju` 与图片并列**（`present_files` 的 `files` 中必须含 `.opju`）
- `related_files` 放脚本与 CSV，**不要**把 `.opju` 只藏在 related
- 保存失败时：先存 ASCII 临时路径再 copy；仍失败则保持 Origin 打开请用户 Ctrl+S，并在回复中说明
- 命名：与图名一致，如 `Fig_6min_combustion.opju`

## 交付

PNG/PDF/TIF + OPJU + `results.txt`（UTF-8）→ `present_files`。  
图上内容以**规范库清单**为准；缺省：轴（变量/量纲）、刻度（含规范要求的次刻度）、关键标注、结果标题。
