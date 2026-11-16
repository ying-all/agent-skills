#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""deepdoc · markdown -> 单文件交互式 HTML 文档

用法：
    python build.py --input note.md --output out.html \
        --title "SQL 注入方法论" --subtitle "从背 payload 到建假设" \
        --chips "17 章|可执行 SOP|速查卡"

依赖：Python 3.8+；Python-Markdown（已随包 vendor），Pygments 可选（有则高亮）。
"""
import argparse
import hashlib
import html
import io
import os
import re
import sys

sys.dont_write_bytecode = True

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, "vendor"))

import markdown  # noqa: E402

try:
    from pygments import highlight
    from pygments.formatters import HtmlFormatter
    from pygments.lexers import (BashLexer, HtmlLexer, HttpLexer, JavaLexer,
                                 JavascriptLexer, JsonLexer, PhpLexer,
                                 PythonLexer, SqlLexer, TextLexer)
    HAS_PYGMENTS = True
except Exception:  # pragma: no cover
    HAS_PYGMENTS = False


# --------------------------------------------------------------------- 代码块
LEXERS = {
    "sql": SqlLexer, "mysql": SqlLexer,
    "php": lambda **k: PhpLexer(startinline=True),
    "bash": BashLexer, "sh": BashLexer, "shell": BashLexer,
    "java": JavaLexer, "http": HttpLexer, "python": PythonLexer,
    "json": JsonLexer, "html": HtmlLexer, "javascript": JavascriptLexer,
    "js": JavascriptLexer, "": TextLexer, "text": TextLexer,
}
LABELS = {
    "sql": "SQL", "mysql": "SQL", "php": "PHP", "bash": "SHELL", "sh": "SHELL",
    "shell": "SHELL", "java": "JAVA", "http": "HTTP", "python": "PYTHON",
    "json": "JSON", "html": "HTML", "javascript": "JS", "js": "JS",
    "text": "TEXT", "": "TEXT",
}
FENCE = re.compile(r"^```([\w+.-]*)[ \t]*\n(.*?)^```[ \t]*$", re.S | re.M)


def render_code(code: str, lang: str) -> str:
    label = LABELS.get(lang, lang.upper())
    if HAS_PYGMENTS and lang in LEXERS:
        try:
            lexer = LEXERS[lang](stripnl=False, stripall=False)
            inner = highlight(code, lexer, HtmlFormatter(cssclass="hl", nowrap=False))
        except Exception:
            inner = "<div class=\"hl\"><pre>" + html.escape(code) + "</pre></div>"
    else:
        inner = "<div class=\"hl\"><pre>" + html.escape(code) + "</pre></div>"
    return (
        '<div class="codeblock"><div class="cb-head"><span class="lang">%s</span>'
        '<button class="copy" type="button" aria-label="复制代码">复制</button></div>'
        '<div class="cb-body">%s</div></div>' % (label, inner)
    )


def slugify(value, separator, *args, **kwargs):
    m = re.match(r"^\s*(\d+(?:\.\d+)*)[\.\s]", value)
    if m:
        return "s" + m.group(1).replace(".", "-")
    m = re.match(r"^\s*阶段\s*([A-Za-z])", value)
    if m:
        return "phase-" + m.group(1).lower()
    v = value.strip()
    if v in ("结语", "总结", "后记"):
        return "conclusion"
    return "sec-" + hashlib.md5(v.encode("utf-8")).hexdigest()[:6]


def split_num(title: str):
    t = re.sub(r"<[^>]+>", "", title)
    m = re.match(r"^(\d+(?:\.\d+)*)[\.\s]+\s*(.*)$", t)
    if m:
        return m.group(1), m.group(2)
    return "", t


def convert(md_text: str):
    blocks = []

    def stash(m):
        blocks.append(render_code(m.group(2), (m.group(1) or "").lower()))
        return "CODEBLOCKPLACEHOLDER%d" % (len(blocks) - 1)

    md_text = FENCE.sub(stash, md_text)

    md = markdown.Markdown(
        extensions=["extra", "sane_lists", "toc"],
        extension_configs={"toc": {"slugify": slugify, "title": "目录"}},
        output_format="html5",
    )
    content = md.convert(md_text)

    content = re.sub(r"<p>CODEBLOCKPLACEHOLDER(\d+)</p>", lambda m: blocks[int(m.group(1))], content)
    content = re.sub(r"CODEBLOCKPLACEHOLDER(\d+)", lambda m: blocks[int(m.group(1))], content)
    content = content.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
    content = content.replace("<blockquote>", '<blockquote class="callout">')
    content = content.replace("<code>\\|\\|</code>", "<code>||</code>")
    content = re.sub(
        r"<li>\[ \] (.*?)</li>",
        r'<li class="task"><label><input type="checkbox"><span>\1</span></label></li>',
        content, flags=re.S,
    )
    content = re.sub(
        r'<h([23]) id="([^"]+)">(.*?)</h\1>',
        lambda m: '<h%s id="%s">%s<a class="anchor" href="#%s" aria-label="本节链接">#</a></h%s>'
                  % (m.group(1), m.group(2), m.group(3), m.group(2), m.group(1)),
        content, flags=re.S,
    )
    return content, md.toc_tokens


def flatten(tokens):
    out = []
    for t in tokens or []:
        out.append(t)
        out.extend(flatten(t.get("children")))
    return out


def build_nav(toc_tokens):
    items, cur = [], None
    for node in flatten(toc_tokens):
        if node["level"] == 2:
            num, title = split_num(node["name"])
            num_span = ('<span class="num">%s</span>' % num) if num else ""
            cur = {"id": node["id"], "num": num, "title": title,
                   "subs": [], "num_span": num_span}
            items.append(cur)
        elif node["level"] == 3 and cur is not None:
            cn, ct = split_num(node["name"])
            cur["subs"].append((cn, ct, node["id"]))
    out = []
    for g in items:
        sub = ""
        if g["subs"]:
            lis = []
            for cn, ct, cid in g["subs"]:
                num_span = ('<span class="num">%s</span>' % cn) if cn else ""
                lis.append('<li><a href="#%s">%s<span class="t">%s</span></a></li>'
                           % (cid, num_span, html.escape(ct)))
            sub = '<ul class="toc-sub">%s</ul>' % "".join(lis)
        caret = '<button class="caret" type="button" aria-label="展开子目录">›</button>' if sub else ""
        out.append(
            '<li class="g" data-for="%s"><div class="toc-row"><a class="toc-h2" href="#%s">%s'
            '<span class="t">%s</span></a>%s</div>%s</li>'
            % (g["id"], g["id"], g["num_span"], html.escape(g["title"]), caret, sub)
        )
    return "\n".join(out)


def build_cards(toc_tokens):
    cards = []
    for node in flatten(toc_tokens):
        if node["level"] != 2:
            continue
        num, title = split_num(node["name"])
        badge = ('<span class="card-num">%s</span>' % num) if num else ""
        cards.append('<a class="card" href="#%s">%s<span class="card-t">%s</span></a>'
                     % (node["id"], badge, html.escape(title)))
    return "\n".join(cards)


def main():
    ap = argparse.ArgumentParser(description="deepdoc: markdown -> 单文件 HTML 文档")
    ap.add_argument("--input", required=True, help="源 markdown")
    ap.add_argument("--output", required=True, help="输出 html")
    ap.add_argument("--title", required=True, help="文档标题")
    ap.add_argument("--subtitle", default="", help="副标题/一句话简介")
    ap.add_argument("--eyebrow", default="Deep Doc", help="标题上方的小字")
    ap.add_argument("--chips", default="", help="元信息标签，用 | 分隔")
    ap.add_argument("--intro", default="", help="开头的说明 markdown 文件（可选）")
    ap.add_argument("--footer", default="本文档为学习笔记，仅用于授权范围内的学习与测试。")
    args = ap.parse_args()

    md_text = io.open(args.input, encoding="utf-8-sig").read()
    content, toc = convert(md_text)
    nav = build_nav(toc)
    cards = build_cards(toc)

    css = io.open(os.path.join(BASE, "doc.css"), encoding="utf-8").read()
    js = io.open(os.path.join(BASE, "doc.js"), encoding="utf-8").read()

    intro = ""
    if args.intro and os.path.exists(args.intro):
        intro_md = io.open(args.intro, encoding="utf-8-sig").read()
        intro_html, _ = convert(intro_md)
        intro = '<blockquote class="callout intro">%s</blockquote>' % intro_html

    chips = "".join('<span class="chip">%s</span>' % html.escape(c.strip())
                    for c in args.chips.split("|") if c.strip())

    doc = """<!doctype html>
<html lang="zh-CN" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="generator" content="deepdoc">
<style>
{css}
</style>
</head>
<body>
<div class="progress" id="progress"></div>
<header class="topbar">
  <button class="btn menu-btn" id="menuBtn" aria-label="打开目录">☰</button>
  <a class="brand" href="#top">{title}</a>
  <div class="top-actions">
    <button class="btn" id="searchBtn">搜索 <kbd>Ctrl K</kbd></button>
    <button class="btn" id="themeBtn" aria-label="切换主题">☾</button>
  </div>
</header>

<div class="layout">
  <aside class="sidebar" id="sidebar">
    <div class="toc-title">目录</div>
    <nav aria-label="章节目录"><ol class="toc">
{nav}
    </ol></nav>
  </aside>
  <div class="scrim" id="scrim"></div>

  <main class="content" id="top">
    <div class="hero">
      <div class="eyebrow">{eyebrow}</div>
      <h1>{title}</h1>
      <p>{subtitle}</p>
      <div class="chips">{chips}</div>
      <div class="cards">
{cards}
      </div>
    </div>
{intro}
{content}
    <footer class="doc-foot">
      <p>{footer}</p>
      <p>由 deepdoc 生成 · 单文件离线可用 · 无外部依赖</p>
    </footer>
  </main>
</div>

<button class="to-top" id="toTop" aria-label="回到顶部">↑</button>

<div class="search-layer" id="searchLayer" role="dialog" aria-modal="true" aria-label="搜索文档">
  <div class="search-box">
    <div class="search-input">
      <span aria-hidden="true">⌕</span>
      <input id="searchInput" type="search" placeholder="搜索章节、关键词、payload…" autocomplete="off" spellcheck="false">
      <span class="hint">ESC</span>
    </div>
    <div class="search-results" id="searchResults"></div>
  </div>
</div>

<script>
{js}
</script>
</body>
</html>
""".format(title=html.escape(args.title), subtitle=html.escape(args.subtitle),
           eyebrow=html.escape(args.eyebrow), chips=chips, nav=nav, cards=cards,
           intro=intro, content=content, css=css, js=js, footer=html.escape(args.footer))

    out_dir = os.path.dirname(os.path.abspath(args.output))
    os.makedirs(out_dir, exist_ok=True)
    io.open(args.output, "w", encoding="utf-8").write(doc)
    print("written: %s  (%.1f KB, %d sections, %d code blocks)"
          % (args.output, len(doc.encode("utf-8")) / 1024,
             sum(1 for t in flatten(toc) if t["level"] == 2), doc.count('class="codeblock"')))


if __name__ == "__main__":
    main()
