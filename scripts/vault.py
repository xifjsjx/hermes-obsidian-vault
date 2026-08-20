#!/usr/bin/env python3
"""Hermes Obsidian 库操作脚本（仅依赖标准库）。

用法：
  python3 vault.py new    <vault> <相对路径.md> [--title T] [--type 盲区] [--subject 数学] [--status 待消化] [--source kimi] [--tags a,b] [--body 正文]
  python3 vault.py find   <vault> <关键词>          # 写笔记前去重：搜标题与正文
  python3 vault.py daily  <vault> [--text 追加内容]  # 追加到今日复盘日记（不存在则创建）
  python3 vault.py index  <vault> [--dir 子目录]     # 重建 MOC 索引笔记
  python3 vault.py orphans <vault>                  # 列出无任何入链的孤立笔记
"""
import argparse
import re
import sys
from datetime import date
from pathlib import Path

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]")


def resolve(vault: Path, rel: str) -> Path:
    p = (vault / rel).resolve()
    if not str(p).startswith(str(vault.resolve())):
        sys.exit(f"错误：路径越出库范围 {rel}")
    if p.suffix != ".md":
        p = p.with_suffix(".md")
    return p


def cmd_new(a):
    vault = Path(a.vault)
    p = resolve(vault, a.path)
    if p.exists():
        print(f"已存在，跳过创建：{p.relative_to(vault)}")
        return
    title = a.title or p.stem
    fm = ["---", f"title: {title}"]
    if a.type: fm.append(f"type: {a.type}")
    if a.subject: fm.append(f"subject: {a.subject}")
    if a.status: fm.append(f"status: {a.status}")
    fm.append(f"created: {date.today().isoformat()}")
    if a.source: fm.append(f"source: {a.source}")
    if a.tags: fm.append(f"tags: [{', '.join(t.strip() for t in a.tags.split(','))}]")
    fm.append("---")
    body = a.body or ""
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("\n".join(fm) + f"\n\n# {title}\n\n{body}\n", encoding="utf-8")
    print(f"已创建：{p.relative_to(vault)}")


def cmd_find(a):
    vault = Path(a.vault)
    kw = a.keyword.lower()
    hits = []
    for p in sorted(vault.rglob("*.md")):
        text = p.read_text(encoding="utf-8", errors="ignore")
        if kw in p.stem.lower() or kw in text.lower():
            lines = [l.strip() for l in text.splitlines() if kw in l.lower()][:3]
            hits.append((p.relative_to(vault), lines))
    if not hits:
        print(f"未找到与「{a.keyword}」相关的笔记，可安全新建。")
        return
    print(f"找到 {len(hits)} 篇相关笔记（写入前请先判断是否应合并而非新建）：")
    for rel, lines in hits:
        print(f"\n■ {rel}")
        for l in lines:
            print(f"    {l[:80]}")


def cmd_daily(a):
    vault = Path(a.vault)
    today = date.today().isoformat()
    p = resolve(vault, f"30-日记/{today}.md")
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(
            f"---\ntitle: {today} 复盘\ntype: 复盘\ncreated: {today}\n---\n\n# {today} 复盘\n",
            encoding="utf-8",
        )
    if a.text:
        with p.open("a", encoding="utf-8") as f:
            f.write(f"\n{a.text}\n")
        print(f"已追加到 {p.relative_to(vault)}")
    else:
        print(p.read_text(encoding="utf-8"))


def cmd_index(a):
    vault = Path(a.vault)
    target = vault / (a.dir or "")
    notes = sorted(p for p in target.rglob("*.md") if "40-MOC" not in p.parts)
    by_dir = {}
    for p in notes:
        by_dir.setdefault(p.parent.relative_to(vault), []).append(p)
    lines = ["---", f"title: {a.dir or '全库'} 索引", "type: MOC",
             f"created: {date.today().isoformat()}", "---", "", f"# {a.dir or '全库'} 索引", ""]
    for d, ps in sorted(by_dir.items(), key=lambda x: str(x[0])):
        lines.append(f"## {d}")
        lines += [f"- [[{p.stem}]]" for p in ps]
        lines.append("")
    out = resolve(vault, f"40-MOC/{(a.dir or '全库')}-索引.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"索引已重建：{out.relative_to(vault)}（{len(notes)} 篇）")


def cmd_orphans(a):
    vault = Path(a.vault)
    notes = list(vault.rglob("*.md"))
    linked = set()
    for p in notes:
        linked.update(t.strip() for t in WIKILINK_RE.findall(p.read_text(encoding="utf-8", errors="ignore")))
    orphans = [p.relative_to(vault) for p in notes
               if p.stem not in linked and "40-MOC" not in p.parts]
    if not orphans:
        print("无孤立笔记，库连接良好。")
        return
    print(f"{len(orphans)} 篇孤立笔记（无任何入链，建议补 wikilink 或归档）：")
    for rel in orphans:
        print(f"  - {rel}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Hermes Obsidian 库操作")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("new"); s.add_argument("vault"); s.add_argument("path")
    s.add_argument("--title"); s.add_argument("--type"); s.add_argument("--subject")
    s.add_argument("--status"); s.add_argument("--source"); s.add_argument("--tags")
    s.add_argument("--body"); s.set_defaults(f=cmd_new)

    s = sub.add_parser("find"); s.add_argument("vault"); s.add_argument("keyword")
    s.set_defaults(f=cmd_find)

    s = sub.add_parser("daily"); s.add_argument("vault"); s.add_argument("--text")
    s.set_defaults(f=cmd_daily)

    s = sub.add_parser("index"); s.add_argument("vault"); s.add_argument("--dir")
    s.set_defaults(f=cmd_index)

    s = sub.add_parser("orphans"); s.add_argument("vault"); s.set_defaults(f=cmd_orphans)

    args = ap.parse_args()
    args.f(args)
