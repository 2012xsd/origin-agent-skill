# -*- coding: utf-8 -*-
"""只读盘点 Origin 项目：python inspect_origin.py project.opju"""
import sys
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("usage: inspect_origin.py <file.opju>")
        return 1
    path = Path(sys.argv[1])
    if not path.exists():
        print("not found", path)
        return 1
    print("file", path, path.stat().st_size, "bytes")
    try:
        import originpro as op
    except ImportError as e:
        print("originpro missing:", e)
        return 1
    try:
        os_system = __import__("os").system
        os_system("taskkill /f /im Origin64.exe >nul 2>&1")
    except Exception:
        pass
    op.set_show(False)
    op.open(str(path).replace("\\", "/"))
    try:
        books = list(op.pages("w"))
        graphs = list(op.pages("g"))
        print("workbooks", len(books), "graphs", len(graphs))
        for i, g in enumerate(graphs):
            try:
                nplots = len(g[0].plot_list())
            except Exception:
                nplots = -1
            print(f"  graph[{i}] name={getattr(g,'name',i)} plots={nplots}")
        return 0
    finally:
        try:
            op.exit()
        except Exception:
            pass

if __name__ == "__main__":
    raise SystemExit(main())
