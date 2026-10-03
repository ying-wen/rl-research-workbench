"""Build and check the handbook's source-to-tool traceability. Standard library only.

The original HTML is an immutable evidence snapshot; all reading/index pages are
derived from it and reviewed JSON mappings. Commands in mappings are parsed, never
executed. A valid link is not a certificate of scientific adequacy.
"""
import argparse
import ast
import contextlib
import hashlib
import html
from html.parser import HTMLParser
import io
import json
import re
import shlex
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from rlworkbench.cli import parser as workbench_parser

SNAPSHOT = "docs/research-handbook.html"
SOURCE_SHA = "1bda47d33d75960c234d521ae4ff2f1dde8d53577ef9a38b0997c655c33b655f"
MAPPINGS = ("chapters-core.json", "chapters-continual.json", "extensions.json")
REPO = "https://github.com/ying-wen/rl-research-workbench/blob/main/"
SUPPORT = {"human_protocol": "人工研究协议", "partial_tooling": "部分工具支持", "implemented_tool": "所述工具已实现"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


class Node:
    def __init__(self, tag="root", attrs=()):
        self.tag, self.attrs, self.children = tag, dict(attrs), []

    def text(self):
        return "".join(c.text() if isinstance(c, Node) else c for c in self.children)

    def walk(self, tag=None):
        if tag is None or self.tag == tag:
            yield self
        for child in self.children:
            if isinstance(child, Node):
                yield from child.walk(tag)


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.root, self.stack = Node(), []
        self.stack.append(self.root)
        self.feed(source)
        self.close()

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def esc(text):
    return re.sub(r"([\\`*_\[\]])", r"\\\1", html.escape(text, quote=False))


def inline(node):
    if isinstance(node, str):
        return esc(node)
    if node.tag in {"script", "style", "input"}:
        return ""
    body = "".join(inline(c) for c in node.children)
    anchor = '<a id="' + node.attrs["id"] + '"></a>' if node.attrs.get("id") else ""
    if node.tag == "br":
        return "<br>"
    if node.tag == "a" and node.attrs.get("href"):
        body = "[" + body + "](" + node.attrs["href"] + ")"
    elif node.tag in {"strong", "b"}:
        body = "**" + body + "**"
    elif node.tag in {"em", "i"}:
        body = "*" + body + "*"
    elif node.tag == "code":
        delimiter = "``" if "`" in node.text() else "`"
        body = delimiter + node.text() + delimiter
    elif node.tag in {"sub", "sup"}:
        body = "<" + node.tag + ">" + body + "</" + node.tag + ">"
    elif node.tag in {"p", "div", "details", "summary", "li"}:
        body = body.strip() + "<br>"
    return anchor + body


def render(node):
    """Preserve the complete source sections, including tables and hidden details."""
    if isinstance(node, str):
        return esc(node)
    if node.tag in {"script", "style", "input"}:
        return ""
    anchor = '\n<a id="' + node.attrs["id"] + '"></a>\n' if node.attrs.get("id") else ""
    if re.fullmatch(r"h[1-6]", node.tag):
        return anchor + "\n" + "#" * int(node.tag[1]) + " " + inline_children(node).strip() + "\n\n"
    if node.tag == "pre" or "equation" in node.attrs.get("class", "").split():
        # br is semantically a line break in displayed equations.
        def plain(n):
            if isinstance(n, str):
                return n
            if n.tag == "br":
                return "\n"
            content = "".join(plain(c) for c in n.children)
            if n.tag in {"sub", "sup"}:
                return ("_" if n.tag == "sub" else "^") + "{" + content + "}"
            return content
        return anchor + "\n```text\n" + plain(node).strip() + "\n```\n\n"
    if node.tag == "table":
        rows = []
        for row in node.walk("tr"):
            cells = [c for c in row.children if isinstance(c, Node) and c.tag in {"th", "td"}]
            values = [inline(c).strip().rstrip("\n").replace("|", "&#124;").replace("\n", " ") for c in cells]
            if row.attrs.get("id") and values:
                values[0] = '<a id="' + row.attrs["id"] + '"></a>' + values[0]
            rows.append(values)
        if not rows:
            return anchor
        lines = ["| " + " | ".join(row) + " |" for row in rows]
        lines.insert(1, "| " + " | ".join(["---"] * len(rows[0])) + " |")
        return anchor + "\n" + "\n".join(lines) + "\n\n"
    if node.tag in {"ol", "ul"}:
        items = []
        for i, child in enumerate(c for c in node.children if isinstance(c, Node) and c.tag == "li"):
            prefix = str(i+1) + ". " if node.tag == "ol" else "- "
            content = "".join(render(c) for c in child.children).strip()
            items.append(prefix + content.replace("\n", "\n" + " " * len(prefix)))
        return anchor + "\n" + "\n".join(items) + "\n\n"
    if node.tag == "label" and list(node.walk("input")):
        return anchor + "- [ ] " + inline_children(node).strip() + "\n"
    if node.tag == "button":
        if node.attrs.get("id") == "download-sources":
            return "\n[" + esc(node.text()) + "](sources.json)\n"
        name = node.attrs.get("data-download")
        if name:
            return "\n- [" + esc(node.text()) + "](../templates/research-handbook/" + name + ")\n"
        return "\n[" + esc(node.text()) + "](handbook/index.html#" + ("ops-checklist" if node.attrs.get("id") == "export-checklist" else "appendix-templates") + ")\n"
    if node.tag == "blockquote":
        return anchor + "\n> " + "".join(render(c) for c in node.children).strip().replace("\n", "\n> ") + "\n\n"
    if node.tag in {"p", "summary"}:
        return anchor + "\n" + inline_children(node).strip() + "\n\n"
    if node.tag in {"a", "strong", "b", "em", "i", "code", "sub", "sup", "br", "span"}:
        return inline(node)
    return anchor + "".join(render(c) for c in node.children) + "\n"


def inline_children(node):
    return "".join(inline(c) for c in node.children)


def source_data(root=ROOT):
    source = (root / SNAPSHOT).read_text(encoding="utf-8")
    sections = list(Document(source).root.walk("section"))
    # Read embedded JSON as data. Never evaluate the original JavaScript.
    templates = json.JSONDecoder().raw_decode(source.split("const templates=", 1)[1])[0]
    sources = json.JSONDecoder().raw_decode(source.split("const sourceRecords=", 1)[1])[0]
    return source, sections, templates, sources


def entries(root=ROOT):
    result = []
    for path in MAPPINGS:
        data = json.loads((root / "docs/traceability" / path).read_text(encoding="utf-8"))
        if data.get("schema_version") != 1:
            raise ValueError("unsupported mapping schema: " + path)
        result.extend(data["entries"])
    return result


def symbols(path):
    found = {}
    def visit(body, prefix=""):
        for node in body:
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                name = prefix + node.name
                found[name] = node.lineno
                visit(node.body, name + ".")
    visit(ast.parse(path.read_text(encoding="utf-8")).body)
    return found


def validate_entries(items, root=ROOT):
    errors, seen = [], set()
    _, sections, _, _ = source_data(root)
    expected = {s.attrs["id"]: next(s.walk("h2")).text().strip() for s in sections}
    chapters = [e["id"] for e in items if e.get("kind") == "chapter"]
    if chapters != list(expected):
        errors.append("chapter coverage/order must exactly match all 37 source sections")
    for e in items:
        identity = e.get("id", "<missing>")
        if identity in seen or not re.fullmatch(r"[a-z0-9-]+", identity):
            errors.append(identity + ": duplicate or invalid ID")
        seen.add(identity)
        for field in ("title", "question", "principle", "gaps"):
            if not e.get(field):
                errors.append(identity + ": missing " + field)
        for field in ("docs", "code", "tests", "commands", "assets", "gaps"):
            if not isinstance(e.get(field), list):
                errors.append(identity + ": expected list " + field)
        if e.get("support") not in SUPPORT:
            errors.append(identity + ": invalid support status")
        if e.get("kind") not in {"chapter", "extension"}:
            errors.append(identity + ": invalid kind")
        if e.get("kind") == "chapter" and expected.get(identity) != e.get("title"):
            errors.append(identity + ": title differs from source")
        if e.get("support") == "implemented_tool" and not all(e.get(k) for k in ("code", "tests", "commands")):
            errors.append(identity + ": implemented tool needs code, tests and commands")
        refs = [{"path": p} for p in e.get("docs", []) + e.get("assets", [])]
        refs += e.get("code", []) + e.get("tests", [])
        for ref in refs:
            path = (root / ref["path"]).resolve()
            if root.resolve() not in path.parents or not path.is_file():
                errors.append(identity + ": missing/unsafe path " + ref["path"])
                continue
            if "symbol" in ref:
                if not ref.get("purpose") or ref["symbol"] not in symbols(path):
                    errors.append(identity + ": missing symbol/purpose " + ref["path"] + ":" + ref["symbol"])
        for command in e.get("commands", []):
            argv = command.get("argv", [])
            if not command.get("purpose") or command.get("mode") not in {"read_only", "creates_files", "runs_smoke"} or not isinstance(command.get("requires"), list):
                errors.append(identity + ": incomplete command metadata")
            if any("{" in arg for arg in argv) and not command.get("requires"):
                errors.append(identity + ": placeholder command requires prerequisites")
            if argv[:3] != ["python3", "-m", "rlworkbench"]:
                errors.append(identity + ": unsupported command prefix")
                continue
            try:
                with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
                    workbench_parser().parse_args(argv[3:])
            except SystemExit as exc:
                if exc.code != 0:
                    errors.append(identity + ": CLI grammar rejected " + shlex.join(argv))
    return errors


def link_ref(ref, root=ROOT):
    line = symbols(root / ref["path"])[ref["symbol"]]
    return "[" + ref["path"] + " · " + ref["symbol"] + "](" + REPO + ref["path"] + "#L" + str(line) + ")"


def md_entry(e, root=ROOT):
    out = ['<a id="' + e["id"] + '"></a>', "## " + e["title"],
           "**问题：** " + e["question"], "**原则：** " + e["principle"],
           "**当前支持：" + SUPPORT[e["support"]] + "。** 状态只描述下列子项；不表示本章全部方法已实现。"]
    if e["kind"] == "chapter":
        out.append("[阅读完整原理](handbook.md#" + e["id"] + ") · [交互阅读版](handbook/index.html#" + e["id"] + ")")
    out.append("**实践文档：** " + " · ".join("[" + p + "](../" + p + ")" for p in e["docs"]))
    for label, key in (("代码职责", "code"), ("对应测试", "tests")):
        out.append("**" + label + "：**")
        out.append("\n".join("- " + link_ref(ref, root) + " — " + ref["purpose"] for ref in e[key]) or "当前无直接实现；按人工研究协议执行。")
    if e["commands"]:
        out.append("**可用命令（从仓库根运行，花括号路径须替换）：**")
        for command in e["commands"]:
            out.append("```bash\n" + shlex.join(command["argv"]) + "\n```")
            out.append(command["purpose"] + " 操作类型：`" + command["mode"] + "`。" + (" 前提：" + "；".join(command["requires"]) if command["requires"] else ""))
    if e["assets"]:
        out.append("**模板与配置：** " + " · ".join("[" + p + "](../" + p + ")" for p in e["assets"]))
    out.append("**能力缺口与结论边界：**\n\n" + "\n".join("- " + gap for gap in e["gaps"]))
    return "\n\n".join(out)


def html_entry(e, root=ROOT):
    def link(path, label=None, fragment=""):
        return '<a href="' + html.escape(REPO + path + fragment) + '">' + html.escape(label or path) + '</a>'
    bits = ['<aside class="implementation-map" aria-label="本章与工具的对应">',
            '<div class="map-label">原理 → 实践 → 代码与证据</div>',
            '<p><strong>' + html.escape(SUPPORT[e["support"]]) + '</strong> · ' + html.escape(e["question"]) + '</p>',
            '<p>' + " · ".join(link(p, Path(p).stem) for p in e["docs"]) + '</p>',
            '<details><summary>展开本章对应的函数、测试、命令和能力缺口</summary>',
            '<p>' + html.escape(e["principle"]) + '</p>']
    for label, key in (("代码职责", "code"), ("对应测试", "tests")):
        bits.append('<p><strong>' + label + '</strong></p><ul>')
        for ref in e[key]:
            line = symbols(root / ref["path"])[ref["symbol"]]
            bits.append('<li>' + link(ref["path"], ref["symbol"], '#L' + str(line)) + ' — ' + html.escape(ref["purpose"]) + '</li>')
        if not e[key]:
            bits.append('<li>当前无直接实现，按人工研究协议执行。</li>')
        bits.append('</ul>')
    for command in e["commands"]:
        bits.append('<pre><code>' + html.escape(shlex.join(command["argv"])) + '</code></pre><p>' + html.escape(command["purpose"] + "（" + command["mode"] + "）" + "；".join(command["requires"])) + '</p>')
    bits.append('<p><strong>能力缺口与结论边界</strong></p><ul>' + ''.join('<li>' + html.escape(g) + '</li>' for g in e["gaps"]) + '</ul>')
    if e["assets"]:
        bits.append('<p>' + " · ".join(link(p, Path(p).name) for p in e["assets"]) + '</p>')
    bits.append('<p>' + link('docs/handbook-code-map.md', '逐章映射', '#' + e["id"]) + ' · ' + link('docs/handbook-code-index.md', '从代码反查原理') + '</p></details></aside>')
    return "\n".join(bits)


def reverse_index(items):
    index = defaultdict(list)
    for e in items:
        for kind in ("docs", "assets", "code", "tests"):
            for ref in e[kind]:
                ref = {"path": ref} if isinstance(ref, str) else ref
                index[ref["path"]].append({"entry_id": e["id"], "title": e["title"], "role": kind, "symbol": ref.get("symbol"), "purpose": ref.get("purpose")})
    return dict(sorted(index.items()))


def products(root=ROOT):
    source, sections, templates, sources = source_data(root)
    items = entries(root)
    by_id = {e["id"]: e for e in items}
    md = ["# 强化学习实验与算法测试手册：完整阅读版", "原手册 37 章全文，保留表格、公式、来源及证据边界。此文件由原始 HTML 与逐章映射生成；请修改原理快照以外的维护源，见 [维护说明](handbook-maintenance.md)。",
          "[整体机制设计](mechanism-design.md) · [逐章代码与工具](handbook-code-map.md) · [代码反查原理](handbook-code-index.md) · [交互 HTML](handbook/index.html) · [原始快照](research-handbook.html)",
          "HTML 提供全文筛选、浏览器本地勾选与导出。下列静态检查表不会自动保存状态；空白研究模板与可执行 CLI 协议分开。",
          "\n".join("- [" + e["title"] + "](#" + e["id"] + ")" for e in items if e["kind"] == "chapter")]
    for section in sections:
        e = by_id[section.attrs["id"]]
        md.append(render(section).strip())
        md.append("> **本章实践连接：" + SUPPORT[e["support"]] + "。** [文档、函数、测试、命令与缺口](handbook-code-map.md#" + e["id"] + ")。" + (" 入口：" + " · ".join("[" + Path(p).stem + "](../" + p + ")" for p in e["docs"][:3]) if e["docs"] else ""))
    mapping = ["# 从手册原理到代码与工具", str(len(sections)) + " 章与 " + str(len(items)-len(sections)) + " 类机制扩展均有明确映射。**人工协议、部分工具支持、所述工具已实现**描述的是支持范围，不是算法效能。所有命令只通过语法核验；带前提的命令需先准备真实数据。", "[全文阅读](handbook.md) · [整体机制设计](mechanism-design.md) · [反向索引](handbook-code-index.md) · [维护说明](handbook-maintenance.md)", "\n".join("- [" + e["title"] + "](#" + e["id"] + ")" for e in items)]
    mapping += [md_entry(e, root) for e in items]
    reverse = reverse_index(items)
    reverse_md = ["# 从代码、测试与协议反查手册", "修改一个文件前，先查看它承接哪些原理、验证哪些子问题。索引覆盖映射中实际引用的文件；没有引用的实现仍须补登记，不能由本工具自动判断完备性。", "[全文](handbook.md) · [逐章映射](handbook-code-map.md) · [机制设计](mechanism-design.md)", "```bash\npython3 scripts/handbook.py find rlworkbench/continual_metrics.py --json\npython3 scripts/handbook.py find GVF\npython3 scripts/handbook.py check\n```"]
    for path, refs in reverse.items():
        reverse_md.append("## " + path + "\n\n[打开文件](../" + path + ")\n\n" + "\n".join("- [" + ref["title"] + "](handbook-code-map.md#" + ref["entry_id"] + ") · `" + ref["role"] + "`" + (" · `" + ref["symbol"] + "` — " + ref["purpose"] if ref["symbol"] else "") for ref in refs))
    extra_css = '''\n.implementation-map{border:1px solid #bfd3c7;border-left:4px solid #277b6d;background:#f0f6f0;border-radius:5px;padding:17px 20px;margin:25px 0 5px;font-size:13px;overflow-wrap:anywhere}.map-label{font-size:11px;letter-spacing:.06em;font-weight:750;color:#316b5e;margin-bottom:8px}.implementation-map p{margin:8px 0}.implementation-map details{font-size:13px}.implementation-map summary{font-weight:650}.implementation-map li{margin:8px 0}.workbench-entry{background:#e5efe7;border:1px solid #b6cdbd;padding:16px 22px;border-radius:6px;margin:0 0 22px;font-size:14px}.workbench-entry p{margin:5px 0}.workbench-entry a{margin-right:12px}@media(max-width:760px){.implementation-map{padding:14px}.workbench-entry{padding:14px}}\n'''
    banner = '<div class="workbench-entry"><strong>RL Research Workbench · 原理与工具一体阅读版</strong><p>保留原手册全部 37 章；每章末尾有代码、测试、命令与能力缺口。先读整体机制设计，再按问题进入实验。</p><p>' + ' '.join('<a href="' + REPO + p + '">' + label + '</a>' for p, label in (("docs/mechanism-design.md", "整体机制设计"), ("docs/handbook.md", "GitHub 全文"), ("docs/handbook-code-map.md", "逐章映射"), ("docs/handbook-code-index.md", "代码反查"), ("README.md", "仓库入口"))) + '</p></div>'
    enhanced = source.replace('</style>', extra_css + '</style>', 1).replace('<main>', '<main>' + banner, 1)
    def inject(match):
        opening, body = match.group(1), match.group(3)
        identity = match.group(2)
        return opening + body + html_entry(by_id[identity], root) + '</section>'
    enhanced = re.sub(r'(<section\b[^>]*\bid="([^"]+)"[^>]*>)([\s\S]*?)</section>', inject, enhanced)
    result = {"docs/handbook.md": "\n\n".join(md) + "\n", "docs/handbook-code-map.md": "\n\n".join(mapping) + "\n", "docs/handbook-code-index.md": "\n\n".join(reverse_md) + "\n", "docs/handbook/index.html": enhanced}
    result.update({"templates/research-handbook/" + name: value for name, value in templates.items()})
    provenance = {"schema_version": 1, "source_snapshot": SNAPSHOT, "source_sha256": SOURCE_SHA, "source_date": "2026-10-03", "chapter_count": len(sections), "source_record_count": len(sources), "template_count": len(templates), "extension_count": len(items)-len(sections), "content_policy": "original HTML preserved byte-for-byte; complete section text converted; code maps are maintained separately", "mapping_files": ["docs/traceability/" + p for p in MAPPINGS]}
    result["docs/traceability/source.json"] = json.dumps(provenance, ensure_ascii=False, indent=2) + "\n"
    result["docs/traceability/index.json"] = json.dumps({"schema_version": 1, "entries": items, "files": reverse}, ensure_ascii=False, indent=2) + "\n"
    return result


def check(root=ROOT):
    errors = []
    if hashlib.sha256((root / SNAPSHOT).read_bytes()).hexdigest() != SOURCE_SHA:
        errors.append("original handbook snapshot digest changed; preserve the evidence source")
    source, sections, _, sources = source_data(root)
    if len(sections) != 37 or len(sources) != 81:
        errors.append("unexpected source coverage")
    if sources != json.loads((root / "docs/sources.json").read_text(encoding="utf-8")):
        errors.append("source register differs from original embedded source records")
    errors += validate_entries(entries(root), root)
    if errors:
        return errors
    for path, expected in products(root).items():
        if not (root / path).is_file() or (root / path).read_text(encoding="utf-8") != expected:
            errors.append(path + ": stale or absent; run python3 scripts/handbook.py build")
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("build", help="regenerate reading pages and indices from reviewed sources")
    sub.add_parser("check", help="read-only coverage, source, AST, CLI and generated-file checks")
    search = sub.add_parser("find", help="find principles, tools and gaps by path, symbol or topic")
    search.add_argument("query")
    search.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if args.command == "find":
        matches = [e for e in entries() if args.query.casefold() in json.dumps(e, ensure_ascii=False).casefold()]
        if args.json:
            print(json.dumps({"query": args.query, "matches": matches}, ensure_ascii=False, indent=2))
        else:
            for e in matches:
                print(e["title"] + " · " + SUPPORT[e["support"]])
                print("  docs/handbook-code-map.md#" + e["id"])
                print("  " + e["question"])
        return 0 if matches else 1
    if args.command == "build":
        errors = validate_entries(entries())
        if hashlib.sha256((ROOT / SNAPSHOT).read_bytes()).hexdigest() != SOURCE_SHA:
            errors.append("original snapshot digest changed")
        if errors:
            print(json.dumps({"status": "failed", "errors": errors}, ensure_ascii=False, indent=2))
            return 1
        output = products()
        for path, content in output.items():
            (ROOT / path).parent.mkdir(parents=True, exist_ok=True)
            (ROOT / path).write_text(content, encoding="utf-8")
        print(json.dumps({"status": "built", "files": len(output), "chapters": 37, "extensions": sum(e["kind"] == "extension" for e in entries())}))
        return 0
    errors = check()
    print(json.dumps({"status": "failed" if errors else "passed", "chapters": 37, "extensions": sum(e["kind"] == "extension" for e in entries()), "errors": errors}, ensure_ascii=False, indent=2))
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
