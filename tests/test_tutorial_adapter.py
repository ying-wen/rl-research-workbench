"""Boundary and population tests for the tutorial external producer."""
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from rlworkbench import core
from rlworkbench.tutorial_adapter import make_protocol, produce


class TutorialAdapterTests(unittest.TestCase):
    def runtime(self, fail=False):
        meta = dict(family="classic", task="fixed_bandit", metric="mean_reward", unit="reward/interaction",
                    higher_better=True, scope="controlled teaching task", sources=["https://incompleteideas.net/book/the-book-2nd.html"],
                    budget={"environment_steps": "steps", "evaluation_steps": 0})
        def run(seed, steps, emit):
            rows = []
            for step in range(1, steps + 1):
                row = dict(step=step, value=seed + step / 10, phase="stationary")
                emit(row)
                rows.append(row)
                if fail and seed == 2 and step == 2:
                    raise ArithmeticError("intentional numerical failure")
            return rows
        modules = {key: SimpleNamespace(META=dict(meta, id=key), run=run) for key in ("base", "candidate")}
        return SimpleNamespace(load=modules.__getitem__, source_hashes=lambda: {"algorithm.py": "fixed"}), modules

    def protocol(self, runtime):
        return make_protocol(runtime, ["base", "candidate"], study_id="tutorial-smoke", seeds=[1, 2],
                             holdout_seeds=[3, 4], steps=4, baseline="base", failure_score=-20)

    def test_complete_population_imports_and_partial_failure_is_retained(self):
        runtime, _ = self.runtime(fail=True)
        lock = core.freeze(self.protocol(runtime), external=True)
        with tempfile.TemporaryDirectory() as temp:
            incoming, imported = Path(temp) / "incoming", Path(temp) / "imported"
            result = produce(lock, runtime, incoming)
            self.assertEqual(len(result["jobs"]), 4)
            failed = core.load(incoming / "candidate--tutorial_task--s2" / "result.json")
            self.assertEqual(failed["status"], "failed")
            self.assertEqual(failed["steps"], 2)
            self.assertEqual(len((incoming / "candidate--tutorial_task--s2" / "events.jsonl").read_text().splitlines()), 2)
            audit = core.import_results(lock, incoming, imported)
            self.assertEqual(audit["counts"]["failed"], 2)
            self.assertEqual(audit["counts"]["completed"], 2)
            with self.assertRaises(FileExistsError):
                produce(lock, runtime, incoming)

    def test_task_and_unit_and_budget_mismatches_are_rejected_before_training(self):
        for field, value in (("task", "another_task"), ("unit", "rmse"), ("budget", {"model_backups": 5})):
            runtime, modules = self.runtime()
            modules["candidate"].META[field] = value
            with self.assertRaises(core.ProtocolError):
                self.protocol(runtime)

    def test_source_drift_rejected_before_creating_attempt(self):
        runtime, _ = self.runtime()
        lock = core.freeze(self.protocol(runtime), external=True)
        runtime.source_hashes = lambda: {"algorithm.py": "changed"}
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp) / "incoming"
            with self.assertRaises(core.ProtocolError):
                produce(lock, runtime, out)
            self.assertFalse(out.exists())

    def test_nonfinite_and_short_horizon_become_failed_receipts(self):
        for nonfinite in (True, False):
            runtime, modules = self.runtime()
            def bad_run(seed, steps, emit):
                rows = [dict(step=1, value=float("nan") if nonfinite else 0.5, phase="stationary")]
                for row in rows:
                    emit(row)
                return rows
            modules["candidate"].run = bad_run
            lock = core.freeze(self.protocol(runtime), external=True)
            with tempfile.TemporaryDirectory() as temp:
                incoming = Path(temp) / "incoming"
                produce(lock, runtime, incoming)
                receipt = core.load(incoming / "candidate--tutorial_task--s1" / "result.json")
                self.assertEqual(receipt["status"], "failed")
                self.assertNotIn("metrics", receipt)


if __name__ == "__main__":
    unittest.main()
