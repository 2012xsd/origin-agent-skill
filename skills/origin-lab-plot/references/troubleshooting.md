# 故障排查

## originpro / 启动

| 症状 | 处理 |
|---|---|
| `ModuleNotFoundError: originpro` | 用 `$env:MIMO_PYTHON`；`pip install --user originpro pywin32` |
| COM 启动失败 / 0x80080005 | 手动开一次 Origin，关掉许可弹窗，再跑；注意 Python/Origin 位数 |
| CreatePage 无效指针 | `taskkill /f /im Origin64.exe` 后新开会话 |
| 会话「关掉了」pages=0 | 不要提前 `op.exit()`；保存拷贝完成后再关 |

## 中文 / 路径

- 导出与 save_fig 一律先 `C:\Temp\OriginCal\`
- 最终目录权限锁 → 带时间戳的文件名重拷
- `utf-8-sig` 写审计 CSV，Excel 打开不乱码

## 导出为空 / 不见文件

1. 看 `save_fig` 返回值与临时文件是否 `size>0`  
2. `gl.rescale()` 是否调用、是否有 plot  
3. 图页是否 activate  
4. 换 `type='png'` 与正斜杠路径  

## 颜色/轴被重置

- Origin 分组、`rescale`、`legend -r` 会冲掉设置 → `reassert_axes_after_rescale`
- 手动色在 group 后失效 → group 之后再设色

## OPJU

- `op.save` 返回 False：先临时 ASCII 路径；仍失败则保持 Origin 开着请用户 Ctrl+S  
- 文件被锁：`项目_20260430_160000.opju`

## 残留 Origin 进程

```powershell
taskkill /f /im Origin64.exe
```

脚本务必 `try/finally: op.exit()`（除非刻意留给用户手存）。

## 无法作图？

先确认：Origin 已装、license 正常、`originpro` 可 import、`op.set_show(True)` 能否弹出窗口。  
**不要**用 matplotlib 冒充 Origin 交付，除非用户明确同意降级。
