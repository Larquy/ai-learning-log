#!/usr/bin/env python3
"""读 README 的「知识地图」表格 → 生成 assets/banner.png 与 assets/progress.png

用法：  python tools/readme_visuals.py
改标题/数字：改下面 CFG 即可，不用重画
"""
import pathlib, shutil, subprocess, sys, tempfile

CFG = {
    "title": "AI 学习记录",
    "sub":   "从零基础 → 大模型训练与推理系统",
    "stat1": "02 / 05", "lab1": "阶 段",
    "stat2": "6",       "lab2": "进 行 中 模 块",
}
BLUE, ORANGE, GREY = "#1B44C8", "#E4593A", "#c3cad6"
ROOT = pathlib.Path(__file__).resolve().parent.parent

def find_edge():
    for n in ("msedge.exe", "microsoft-edge", "google-chrome", "chrome"):
        p = shutil.which(n)
        if p:
            return p
    for p in (r"/mnt/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
              r"/mnt/c/Program Files/Microsoft/Edge/Application/msedge.exe",
              r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"):
        if pathlib.Path(p).exists():
            return p
    return None

def to_win(p):
    s = str(p)
    if s.startswith("/mnt/c/"):
        return "C:\\" + s[7:].replace("/", "\\")
    return s.replace("/", "\\")

def render(html, out_png, w, h):
    edge = find_edge()
    if not edge:
        print("⚠️ 找不到 Edge/Chrome，跳过渲染"); return False
    tmp = pathlib.Path(tempfile.mkdtemp())
    f = tmp / "x.html"; f.write_text(html, encoding="utf-8")
    out_png.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([edge, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    f"--window-size={w},{h}", f"--screenshot={to_win(out_png)}",
                    to_win(f)], capture_output=True)
    print("✓", out_png.relative_to(ROOT), out_png.stat().st_size, "bytes")
    return out_png.exists()

def parse_rows(text):
    rows = []
    for line in text.splitlines():
        if not line.startswith("| ") or "`" not in line:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        name, st = cells[0], cells[1]
        for mark, v, lab, col in (("✅",1.0,"已 掌 握",BLUE),
                                  ("🟡",0.55,"进 行 中",ORANGE),
                                  ("⬜",0.0,"未 开 始",GREY)):
            if mark in st:
                rows.append((name, v, lab, col)); break
    return rows

def banner_html(c):
    return f'''<html><head><meta charset="utf-8"><style>
html,body{{margin:0;padding:0}}
.wrap{{width:1200px;height:240px;background:#fff;font-family:"Microsoft YaHei",sans-serif;position:relative;border-bottom:6px solid {BLUE}}}
.accent{{position:absolute;left:0;top:0;width:12px;height:240px;background:{BLUE}}}
h1{{margin:0;padding:58px 0 0 68px;font-size:58px;letter-spacing:3px;color:#12203a}}
.sub{{padding:16px 0 0 72px;font-size:22px;color:#6b7893}}
.right{{position:absolute;right:68px;top:56px;text-align:right}}
.stat{{font-size:42px;font-weight:700;color:{BLUE};font-family:Consolas,monospace}}
.stat2{{font-size:42px;font-weight:700;color:{ORANGE};font-family:Consolas,monospace}}
.lab{{font-size:15px;color:#8792a8;letter-spacing:2px;margin-top:2px}}
</style></head><body><div class="wrap"><div class="accent"></div>
<h1>{c["title"]}</h1><div class="sub">{c["sub"]}</div>
<div class="right"><div class="stat">{c["stat1"]}</div><div class="lab">{c["lab1"]}</div>
<div class="stat2" style="margin-top:14px">{c["stat2"]}</div><div class="lab">{c["lab2"]}</div></div>
</div></body></html>'''

def progress_html(rows):
    h = 44 + 34 + 3 + 30 + len(rows) * 52 + 40
    body = "".join(
        f'<div class="row"><div class="nm">{n}</div><div class="track">'
        f'<div class="fill" style="width:{v*520:.0f}px;background:{c}"></div></div>'
        f'<div class="st">{lab}</div></div>' for n, v, lab, c in rows)
    html = f'''<html><head><meta charset="utf-8"><style>
html,body{{margin:0;padding:0;font-family:"Microsoft YaHei",sans-serif;background:#fff}}
.wrap{{width:1180px;padding:44px 44px 36px}}
.hd{{font-size:34px;font-weight:700;color:#12203a;letter-spacing:2px}}
.rule{{height:3px;background:{BLUE};margin:18px 0 30px;width:120px}}
.row{{display:flex;align-items:center;height:52px}}
.nm{{width:400px;font-size:21px;color:#26314a}}
.track{{width:520px;height:18px;background:#eef1f6;border-radius:9px;overflow:hidden}}
.fill{{height:18px;border-radius:9px}}
.st{{width:150px;text-align:right;font-size:17px;color:#8792a8;letter-spacing:1px}}
</style></head><body><div class="wrap">
<div class="hd">知识地图 &middot; 学习进度</div><div class="rule"></div>
{body}</div></body></html>'''
    return html, h

def main():
    readme = ROOT / "README.md"
    rows = parse_rows(readme.read_text(encoding="utf-8"))
    if not rows:
        print("⚠️ README 里没找到「知识地图」表格（表格第二列要有 ✅/🟡/⬜）")
        sys.exit(1)
    render(banner_html(CFG), ROOT / "assets/banner.png", 1200, 246)
    html, h = progress_html(rows)
    render(html, ROOT / "assets/progress.png", 1180, h)
    print(f"共 {len(rows)} 个模块")

if __name__ == "__main__":
    main()
