---
name: lab-graph-standards
icon: "📏"
description: Use when the user asks to plot under specific experiment graphing rules / 作图规范、按某实验的作图要求出图、课程作图标准（量热/燃烧热、次刻度、图名、雷诺作图法等）。 Loads a per-experiment standards profile and lists the mandatory figure rules before drawing. Do not use for generic Origin API how-to; pair with origin-lab-plot for execution. Profiles live in standards/<experiment>.md — add a new file for a new lab instead of changing the engine skill.
---

# lab-graph-standards（实验作图规范库）

按**实验**分类存放作图要求。换实验 = 加规范文件，**不改**出图引擎（`origin-lab-plot`）。

## 用法

1. 用户指定实验名或「按某实验规范作图」→ 打开  
   `standards/<experiment>.md`
2. **先列规范清单**给用户确认，再调用 `origin-lab-plot` 出图
3. 新实验：复制结构，新建 `standards/<new-lab>.md`，更新本文件「目录」

## 目录（profiles）

| 文件 | 实验 | 状态 |
|---|---|---|
| `standards/calorimetry.md` | 量热 / 燃烧热 ΔT–t（本课程 9 条 + 6 min / 雷诺） | ✅ 2026-09-26 |
| `_template.md` | 新实验骨架 | 空模板 |

未匹配到目录时：问用户是哪门课/哪次实验，或读用户粘贴的规范原文。


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


## 交付时必给 Origin 源文件（.opju）

用户明确要求：**每次出图都附上可编辑的 `.opju` 源文件**，不能只给 PNG/PDF。

- 主交付列表里 **`.opju` 与图片并列**（`present_files` 的 `files` 中必须含 `.opju`）
- `related_files` 放脚本与 CSV，**不要**把 `.opju` 只藏在 related
- 保存失败时：先存 ASCII 临时路径再 copy；仍失败则保持 Origin 打开请用户 Ctrl+S，并在回复中说明
- 命名：与图名一致，如 `Fig_6min_combustion.opju`

## 与 origin-lab-plot 的分工

| | 本 skill | origin-lab-plot |
|---|---|---|
| 职责 | **要什么图**（规范、图上必标、ΔT 怎么算） | **怎么画**（originpro、导出、轴契约） |
| 变化频率 | 每个实验可能不同 | 相对稳定 |

出图时：规范 → 引擎 → 交付。

## 维护

- 改规范只改 `standards/*.md`，不要写进引擎 SKILL.md
- 规范变更需更新文件内 `updated` 日期

### 数值格式（本课程要求）

- **Q_v,m（燃烧热）保留 5 位小数**，单位 kJ/mol（同时可给 J/mol）
- ΔT、T1、T2 保留 4 位小数
- 相对偏差保留 2 位小数
