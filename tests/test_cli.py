import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from rlworkbench.cli import main
from rlworkbench.core import ROOT, load, write_new


class CLITests(unittest.TestCase):
    def call(self, *args):
        output, error = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
            code = main(list(map(str, args)))
        return code, output.getvalue(), error.getvalue()

    def test_documented_full_path_and_budget_summary(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp)
            self.assertEqual(self.call("init", "--profile", "classic", "--out", p/"study.json")[0], 0)
            code, out, _ = self.call("plan", p/"study.json", "--summary")
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(out)["jobs"], 4)
            self.assertEqual(self.call("freeze", p/"study.json", "--out", p/"lock.json")[0], 0)
            self.assertEqual(self.call("run", p/"lock.json", "--out", p/"run")[0], 0)
            self.assertEqual(self.call("audit", p/"run")[0], 0)
            self.assertEqual(self.call("report", p/"run", "--out", p/"report.md")[0], 0)
            self.assertEqual(self.call("compare", p/"run", "--candidate", "sarsa", "--baseline", "q_learning", "--bootstrap", 100)[0], 0)
            self.assertEqual(self.call("run", p/"lock.json", "--out", p/"run")[0], 2)

    def test_recovery_cli_checks_clock_and_completed_horizon(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp)/"events.jsonl"
            rewards = [1, 1, 0, 0, 1, 1]
            p.write_text("\n".join(json.dumps({"type":"transition", "stream":"training", "env_step":i+1, "reward":r}) for i,r in enumerate(rewards)))
            args = ("continual-metrics", p, "--changes", "2", "--window", 2, "--planned-steps", 6)
            code, out, _ = self.call(*args)
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(out)["recoveries"][0]["confirmation_step"], 6)
            p.write_text(p.read_text().replace('"env_step": 4','"env_step": 9'))
            self.assertEqual(self.call(*args)[0], 2)

    def test_module_design_validation_is_not_native_execution(self):
        contract = load(ROOT/"templates/module-contract.json")
        self.assertEqual(self.call("validate-modules", ROOT/"templates/module-contract.json")[0], 0)
        p = load(ROOT/"profiles/classic.json")
        p["modules"] = contract["modules"]
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/"module.json"
            write_new(path, p)
            self.assertEqual(self.call("validate", path)[0], 2)
            self.assertEqual(self.call("validate", path, "--external")[0], 0)


if __name__ == "__main__":
    unittest.main()
