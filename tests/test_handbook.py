"""Guard the handbook's evidence coverage and executable traceability.

These checks prevent dropped source material and misleading code links. They do
not claim the research protocols, numerical methods, or algorithms are effective.
"""
import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("workbench_handbook", ROOT / "scripts/handbook.py")
handbook = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(handbook)


def compact(text):
    text = re.sub(r"</?(?:br|sub|sup|a)\b[^>]*>", "", text)
    text = re.sub(r"[_^]\{([^{}]*)\}", r"\1", text)
    return re.sub(r"\s+", "", text)


class HandbookTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source, cls.sections, cls.templates, cls.sources = handbook.source_data()
        cls.items = handbook.entries()
        cls.products = handbook.products()

    def test_all_original_chapters_have_ordered_reviewed_mappings(self):
        chapters = [e for e in self.items if e["kind"] == "chapter"]
        self.assertEqual(len(self.sections), 37)
        self.assertEqual(len(self.sources), 81)
        self.assertEqual([e["id"] for e in chapters], [s.attrs["id"] for s in self.sections])
        self.assertEqual(handbook.validate_entries(self.items), [])
        self.assertEqual(hashlib.sha256((ROOT / handbook.SNAPSHOT).read_bytes()).hexdigest(), handbook.SOURCE_SHA)
        # Proposed capabilities remain explicit, even where neighbouring tools exist.
        by_id = {e["id"]: e for e in self.items}
        for chapter in ("stats-hpo", "stats-power", "stats-aggregate", "alg-deep"):
            self.assertNotEqual(by_id[chapter]["support"], "implemented_tool")
            self.assertTrue(by_id[chapter]["gaps"])

    def test_removed_chapter_or_nonexistent_symbol_cannot_pass(self):
        missing = [e for e in self.items if e["id"] != "stats-power"]
        self.assertTrue(any("coverage" in error for error in handbook.validate_entries(missing)))
        bad = copy.deepcopy(self.items)
        entry = next(e for e in bad if e["id"] == "guide-objective")
        entry["code"][0]["symbol"] = "this_function_does_not_exist"
        errors = handbook.validate_entries(bad)
        self.assertTrue(any("guide-objective" in error and "missing symbol" in error for error in errors))

    def test_invalid_cli_and_unprepared_placeholders_cannot_pass(self):
        bad = copy.deepcopy(self.items)
        entry = next(e for e in bad if e["commands"])
        entry["commands"][0]["argv"] = ["python3", "-m", "rlworkbench", "invented-auto-hpo"]
        self.assertTrue(any("CLI grammar rejected" in error for error in handbook.validate_entries(bad)))
        bad = copy.deepcopy(self.items)
        entry = next(e for e in bad if e["commands"])
        entry["commands"][0].update(argv=["python3", "-m", "rlworkbench", "audit", "{RUN_DIR}"], requires=[])
        self.assertTrue(any("prerequisites" in error for error in handbook.validate_entries(bad)))

    def test_help_is_valid_documented_cli_without_executing_a_workload(self):
        items = copy.deepcopy(self.items)
        command = next(e["commands"][0] for e in items if e["commands"])
        command.update(argv=["python3", "-m", "rlworkbench", "--help"], requires=[])
        with contextlib.redirect_stdout(io.StringIO()) as output:
            errors = handbook.validate_entries(items)
        self.assertEqual(errors, [])
        self.assertEqual(output.getvalue(), "")

    def test_enhanced_html_keeps_every_original_section_before_adding_maps(self):
        enhanced = list(handbook.Document(self.products["docs/handbook/index.html"]).root.walk("section"))
        self.assertEqual(len(enhanced), len(self.sections))
        for original, output in zip(self.sections, enhanced):
            with self.subTest(chapter=original.attrs["id"]):
                self.assertEqual(output.attrs["id"], original.attrs["id"])
                maps = [child for child in output.children
                        if isinstance(child, handbook.Node)
                        and "implementation-map" in child.attrs.get("class", "").split()]
                self.assertEqual(len(maps), 1)
                # Compare the complete text tree, including collapsed source details,
                # before considering any of the new explanatory content.
                output.children = [child for child in output.children if child not in maps]
                self.assertEqual(output.text(), original.text())
                for tag in ("table", "details", "pre", "ol", "ul", "label", "input"):
                    self.assertEqual(len(list(output.walk(tag))), len(list(original.walk(tag))))

    def test_markdown_preserves_equations_code_details_tables_lists_and_checklist(self):
        md = self.products["docs/handbook.md"]
        nodes = [node for section in self.sections for node in section.walk()]
        tables = [n for n in nodes if n.tag == "table"]
        self.assertEqual(len(re.findall(r"^\| ---", md, re.MULTILINE)), len(tables))
        for node in nodes:
            if node.tag == "pre":
                self.assertTrue("```text\n" + node.text().strip() + "\n```" in md, "source pre block disappeared")
            elif "equation" in node.attrs.get("class", "").split():
                self.assertTrue(compact(node.text()) in compact(md), "source content disappeared: " + node.text()[:120])
            elif node.tag == "details":
                # The source catalogue's collapsed verification scope remains
                # readable in GitHub's static version; it cannot disappear.
                self.assertTrue(compact(node.text()) in compact(md), "source content disappeared: " + node.text()[:120])
        checklist = [n for n in nodes if n.tag == "label" and list(n.walk("input"))]
        self.assertEqual(len(re.findall(r"^- \[ \] ", md, re.MULTILINE)), len(checklist))
        self.assertTrue("1. **精确定义症状。**" in md, "ordered action list disappeared")
        self.assertTrue("- **Bandit：**" in md, "algorithm checklist disappeared")
        # A renderer regression involving nested lists or a table's literal pipe
        # would alter meaning while leaving all top-level chapter counts intact.
        fixture = handbook.Document('<section id="fixture"><table><tr><th>A</th><th>B</th></tr>'
            '<tr><td>left|right</td><td>keep</td></tr></table>'
            '<details><summary>hidden heading</summary><p>hidden evidence</p></details>'
            '<ol><li>outer<ul><li>inner</li></ul></li></ol>'
            '<div class="equation">x=1<br>y=2</div>'
            '<div class="equation">a<sub>t+1</sub>+b<sup>2</sup></div><pre>a &lt; b</pre>'
            '<label><input type="checkbox">manual gate</label>'
            '<a href="https://example.invalid/paper?x=1&amp;y=2">cited result</a></section>')
        converted = handbook.render(fixture.root)
        for marker in ("left&#124;right", "hidden heading", "hidden evidence", "1. outer", "- inner",
                       "x=1\ny=2", "a_{t+1}+b^{2}", "a < b", "- [ ] manual gate",
                       "[cited result](https://example.invalid/paper?x=1&y=2)"):
            self.assertIn(marker, converted)

    def test_chapter_and_source_anchors_are_reachable_from_both_directions(self):
        md = self.products["docs/handbook.md"]
        mapping = self.products["docs/handbook-code-map.md"]
        reverse = self.products["docs/handbook-code-index.md"]
        index = json.loads(self.products["docs/traceability/index.json"])
        for section in self.sections:
            identity = section.attrs["id"]
            self.assertIn('<a id="' + identity + '"></a>', md)
            self.assertIn('<a id="' + identity + '"></a>', mapping)
            self.assertIn("handbook.md#" + identity, mapping)
            self.assertIn("handbook-code-map.md#" + identity, md)
        for node in self.sections[-1].walk():
            if node.attrs.get("id") and node.tag not in {"button", "input"}:
                self.assertIn('<a id="' + node.attrs["id"] + '"></a>', md)
        self.assertTrue("[下载完整来源 JSON](sources.json)" in md, "source download routed to wrong asset")
        for source in self.sources:
            self.assertTrue("](" + source["url"] + ")" in md, "source link disappeared: " + source["id"])
        refs = index["files"]["rlworkbench/analysis.py"]
        self.assertTrue(any(r["entry_id"] == "stats-intervals" and r["symbol"] == "paired_interval" for r in refs))
        self.assertIn("handbook-code-map.md#stats-intervals", reverse)
        for refs in index["files"].values():
            for ref in refs:
                self.assertIn('<a id="' + ref["entry_id"] + '"></a>', mapping)

    def test_find_json_resolves_paths_symbols_and_empty_queries(self):
        for query, expected in (("rlworkbench/analysis.py", "stats-intervals"),
                                ("paired_interval", "stats-intervals")):
            with self.subTest(query=query), contextlib.redirect_stdout(io.StringIO()) as output:
                code = handbook.main(["find", query, "--json"])
                data = json.loads(output.getvalue())
                self.assertEqual(code, 0)
                self.assertEqual(data["query"], query)
                self.assertIn(expected, [e["id"] for e in data["matches"]])
        with contextlib.redirect_stdout(io.StringIO()) as output:
            code = handbook.main(["find", "no-such-handbook-topic-716492", "--json"])
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(output.getvalue())["matches"], [])

    def test_exported_research_templates_are_exact_source_assets(self):
        self.assertEqual(len(self.templates), 6)
        self.assertEqual(json.loads((ROOT / "docs/sources.json").read_text()), self.sources)
        for name, payload in self.templates.items():
            self.assertEqual(self.products["templates/research-handbook/" + name], payload)
        provenance = json.loads(self.products["docs/traceability/source.json"])
        self.assertEqual(provenance["source_sha256"], handbook.SOURCE_SHA)
        self.assertEqual(provenance["chapter_count"], 37)
        self.assertEqual(provenance["source_record_count"], 81)


if __name__ == "__main__":
    unittest.main()
