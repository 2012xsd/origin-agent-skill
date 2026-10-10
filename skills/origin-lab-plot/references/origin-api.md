# originpro API 与禁止事项

## 会话

```python
import originpro as op
op.set_show(True)     # 显示 Origin
op.new()              # 新项目（可选）
op.exit()             # finally 中关闭，避免残留进程
```

## 数据

```python
wks = op.new_sheet()                  # 推荐
# 或 wb = op.new_book('w', 'LName'); wks = wb[0]  （勿用 new_book('Name')）
wks.cols = 6
wks.from_list(0, xs, 't', 'min', axis='X')
wks.from_list(1, ys, 'T', 'K', axis='Y')
wks.from_df(df)                       # pandas
wks.cols_axis('xyy', c1=0, repeat=False)  # 确定列序后再设
```

## 图

```python
gp = op.new_graph('Fig', template='LINESYMB')  # 库内实名
gl = gp[0]
p = gl.add_plot(wks, coly=1, colx=0, type='linesymbol')  # type 小写
# type: linesymbol=line | scatter=s | column=c | area=area
p.color = 1
p.lt_exec('line.width = 2; symbol.size = 5;')
gl.rescale()
gl.set_xlim(0, 20); gl.set_ylim(-0.1, 1.6)
gl.add_line(x1, y1, x2, y2)
gl.add_label('text', x=, y=)
gp.activate()
gp.lt_exec('xb.text$ = "t / min";')
gp.lt_exec('yl.text$ = "\\g(D)T / K";')
gp.lt_exec('label -s -sa -n title "..."')
```

模板名：`os.listdir(op.path('e'))` 过滤 `.otp/.otpu`。常见：`LINESYMB` `LINE` `SCATTER` `COLUMN`。

## 导出与保存

| 方法 | 结果 |
|---|---|
| `gp.save_fig(path, type='png', width=1600)` | ✅ 主路径 |
| `expGraph` | ❌ 常静默失败 |
| `op.save(path)` | ⚠️ 可能 False；先 ASCII 临时目录再 copy |
| COM `save -i` | ❌ 崩溃 |

中文路径：一律 `C:/Temp/OriginCal/` → `shutil.copy2` 目标。

## 定位项目

```python
list(op.pages('w'))   # 工作簿
list(op.pages('g'))   # 图
g[0].plot_list()      # 层数不能当可迭代
```

## 踩坑清单（本机验证）

1. `type='LineSymbol'` → 小写 `linesymbol`
2. `template='LineSymbol'` → `LINESYMB`
3. `new_book('Calorimetry')` → `new_book(type='w', lname=...)` 或 `new_sheet()`
4. PowerShell 哈希表 `t_list`/`T_list` 不分大小写
5. 双引号 here-string 吃掉 LabTalk 的 `$`
6. Origin 脏会话 → 先 `taskkill /f /im Origin64.exe`
7. `rescale`/`legend` 后轴设置被重置 → 再刷 `apply_lab_axes`
8. `pages()` 返回生成器 → `list(...)`；否则 print 无内容

## COM 旁路（originpro 不可用时）

`Origin.Application` → `Execute(LabTalk)` → `Evaluate`。可靠：`col(1)={...}`、`plotxy`、`xb.text$`。  
不可靠：`expGraph`、`save -i`、`exec *.ogs`。
