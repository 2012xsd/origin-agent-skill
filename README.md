# origin-agent-skill

> **本仓库是一套让 AI Agent 自动操作 OriginLab Origin / OriginPro 的技能包。**
> A set of skills that let an AI agent drive OriginLab Origin / OriginPro automatically — from reading data to publishing-grade figures and editable `.opju` projects.

---

## 它是做什么的 / What it does

把「原始实验数据 → 作图 → 导出」整条链路交给 Agent 完成，**不需要人工点鼠标**：

1. 读取 Excel / CSV / 粘贴数据
2. 线性拟合、算 ΔT（6 min 垂线法 / 雷诺等面积法）、算燃烧热与总热容
3. 通过 **`originpro` + COM** 驱动本机 Origin，按作图规范出图
4. 导出 **可编辑 `.opju`** + PNG / PDF / TIF
5. 按实验规范标注（轴名与量纲、主次刻度、关键坐标、拟合结果表）

Agent 只需一句话即可开始：`用 origin-lab-plot 画图，数据在 xxx.csv`

---

## 两个 Skill / Two Skills

| Skill | 职责 | 目录 |
|---|---|---|
| **`origin-lab-plot`** | **怎么画**：Origin 引擎、轴契约、导出、验收 | [`skills/origin-lab-plot`](skills/origin-lab-plot/) |
| **`lab-graph-standards`** | **要什么图**：按实验分类的作图规范库 | [`skills/lab-graph-standards`](skills/lab-graph-standards/) |

分工：`lab-graph-standards` 先给出规范清单 → `origin-lab-plot` 执行出图 → 交付 `.opju` + 图片。

### origin-lab-plot 内容

```
SKILL.md                     # 金流程、API 避坑、图型速查
scripts/
  plot_xy_template.py        # 通用 XY 图模板（改数据即用）
  plot_bar_template.py       # 柱状/分组柱模板
  apply_style.py             # 轴契约 / 四边框 / 次刻度 / 样式
  calc_dt.py                 # 6 min 法 + 雷诺法求 ΔT
  inspect_origin.py          # 只读盘点 .opju
references/
  origin-api.md              # originpro API 与禁止事项
  style-contracts.md         # 轴契约与出版样式
  lab-standards.md           # 实验作图规范（指针）
  troubleshooting.md         # 中文路径 / 锁文件 / 导出失败
```

### lab-graph-standards 内容

```
SKILL.md
standards/
  calorimetry.md             # 量热实验 9 条作图规范 + ΔT + 燃烧热
  _template.md               # 新实验规范骨架
```

---

## 环境要求 / Requirements

| 项 | 说明 |
|---|---|
| OS | **Windows**（Origin 无 macOS/Linux 版） |
| Origin | Origin / OriginPro **2021 及以上**（已在 **2026b** 验证） |
| Python | 3.10+，安装 `originpro` `pywin32` `numpy` `pandas` |

```bash
pip install originpro pywin32 numpy pandas
```

Origin 路径按本机实际配置，写在 `SKILL.md` 的「环境」一节。

---

## 安装 / Installation

MiMo Code / Claude Code 类 skill 目录：

```powershell
# 全局（所有项目可用）
Copy-Item -Recurse skills\origin-lab-plot    "$env:USERPROFILE\.config\mimocode\skills\origin-lab-plot"
Copy-Item -Recurse skills\lab-graph-standards "$env:USERPROFILE\.config\mimocode\skills\lab-graph-standards"
```

---

## 使用 / Usage

新对话里对 Agent 说：

```
用 origin-lab-plot 画图，数据在 D:\data\run1.xlsx
```

```
按作图规范用 6 min 垂线法算 ΔT 并出图，标题写「燃烧热」
```

```
用 origin-lab-plot 画柱状图，要求四边框出版样式
```

Agent 会自动读 `SKILL.md`，按需加载 `references/` 与 `scripts/`，执行完毕交付 `.opju` + 图片。

---

## 关键设计 / Design Notes

- **渐进披露**：主 `SKILL.md` 只放金流程与禁令，细节进 `references/`，省 token
- **规范可插拔**：换实验只新增 `standards/<实验>.md`，不改引擎 skill
- **中文路径默认策略**：先写 ASCII 临时目录再 `copy2`，避免 Origin 导出失败
- **硬性禁止**：`expGraph` 静默失败、COM `save -i` 崩溃、matplotlib 冒充 Origin

---

## License

MIT（脚本与文档可自由使用与修改）
