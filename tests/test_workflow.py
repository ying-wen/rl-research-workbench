import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from rlworkbench import core
from rlworkbench.analysis import compare, markdown_report, paired_interval


def protocol():
    p = core.load(core.ROOT / "profiles/continual.json")
    p["budget"]["steps"] = 20
    return p


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_all_profiles_and_exact_population(self):
        for file in (core.ROOT / "profiles").glob("*.json"):
            p = core.load(file)
            self.assertEqual(core.validate(p), [])
            self.assertEqual(len(core.plan(p)), len(p["arms"])*len(p["envs"])*len(p["seeds"]))

    def test_invalid_fields_rejected_before_execution(self):
        edits = [("seeds", [1, 1]), ("seeds", [True, 2]), ("seeds", [1]),
                 ("seeds", ["x", 2]), ("schema_version", True), ("arms", []),
                 ("minimum_effect", float("nan")), ("baseline_ids", ["missing"]),
                 ("primary_metric", "unknown"), ("budget", {"steps": 1})]
        for key, value in edits:
            p = protocol()
            p[key] = value
            self.assertTrue(core.validate(p), (key, value))

    def test_overlap_and_budget_overrun_rejected(self):
        p = protocol()
        p["holdout_seeds"] = p["seeds"]
        self.assertTrue(core.validate(p))
        p = protocol()
        p["budget"]["max_total_steps"] = 1
        self.assertTrue(core.validate(p))

    def test_freeze_binds_config_jobs_and_source(self):
        lock = core.freeze(protocol())
        core.verify_lock(lock, current_source=True)
        for edit in ("protocol", "jobs", "source"):
            bad = copy.deepcopy(lock)
            if edit == "protocol":
                bad["protocol"]["seeds"] = [99, 100]
            elif edit == "jobs":
                bad["jobs"].pop()
            else:
                bad["source_files"]["rlworkbench/core.py"] = "invalid"
                bad["lock_sha256"] = core.digest({k:v for k,v in bad.items() if k != "lock_sha256"})
            with self.assertRaises(core.ProtocolError):
                core.verify_lock(bad, current_source=True)

    def test_run_and_receipts_reconcile(self):
        lock = core.freeze(protocol())
        out = self.root / "run"
        data = core.run(lock, out)
        self.assertTrue(data["population_complete"])
        self.assertEqual(data["counts"]["completed"], len(lock["jobs"]))
        for row in data["rows"]:
            events = [json.loads(x) for x in (out/"jobs"/row["job_id"]/"events.jsonl").read_text().splitlines()]
            rewards = [x["reward"] for x in events if x.get("type") == "transition"]
            self.assertEqual(len(rewards), 20)
            self.assertAlmostEqual(sum(rewards)/20, row["score"])
        self.assertIn("workflow_smoke_only", markdown_report(out))
        with self.assertRaises(FileExistsError):
            core.run(lock, out)

    def test_failed_jobs_are_kept_not_dropped(self):
        lock = core.freeze(protocol())
        out = self.root / "failure"
        from rlworkbench.engines import execute
        def fail_one(job, directory):
            if job["job_id"] == lock["jobs"][0]["job_id"]:
                (directory/"partial.txt").write_text("original failure evidence")
                raise ArithmeticError("nonfinite parameter")
            return execute(job, directory)
        with patch("rlworkbench.engines.execute", side_effect=fail_one):
            data = core.run(lock, out)
        self.assertTrue(data["population_complete"])
        self.assertEqual(data["counts"]["failed"], 1)
        failed = data["rows"][0]
        self.assertEqual(failed["score"], lock["protocol"]["failure_policy"]["score_floor"])
        self.assertEqual(failed["failure"]["type"], "ArithmeticError")
        result = compare(out, lock["protocol"]["arms"][1]["id"], lock["protocol"]["baseline_ids"][0], repetitions=100)
        self.assertEqual(result["environments"][0]["n_pairs"], 2)

    def test_missing_jobs_cannot_be_silently_scored(self):
        lock = core.freeze(protocol())
        out = self.root / "partial"
        out.mkdir()
        core.write_new(out/"lock.json", lock)
        data = core.audit(out)
        self.assertFalse(data["population_complete"])
        self.assertEqual(data["counts"]["missing"], len(lock["jobs"]))
        with self.assertRaises(core.ProtocolError):
            compare(out, lock["protocol"]["arms"][1]["id"], lock["protocol"]["baseline_ids"][0])

    def test_modified_result_or_artifacts_invalidate_job(self):
        lock = core.freeze(protocol())
        out = self.root / "tamper"
        core.run(lock, out)
        first = out/"jobs"/lock["jobs"][0]["job_id"]
        (first/"events.jsonl").write_text("different events")
        self.assertEqual(core.audit(out)["counts"]["invalid"], 1)
        second = out/"jobs"/lock["jobs"][1]["job_id"]/"result.json"
        result = core.load(second)
        result["metrics"]["mean_reward"] = 1e9
        second.write_text(json.dumps(result))
        self.assertEqual(core.audit(out)["counts"]["invalid"], 2)

    def test_paired_statistics_constant_difference_and_direction(self):
        self.assertEqual(paired_interval([3, 3, 3], repetitions=100), [3, 3])
        with self.assertRaises(core.ProtocolError):
            paired_interval([1], repetitions=100)
        p = protocol()
        p["direction"] = "minimize"
        lock = core.freeze(p)
        scores = {p["arms"][0]["id"]: 5, p["arms"][1]["id"]: 2}
        def fixed(job, directory):
            return {"metrics": {"mean_reward": scores[job["arm"]["id"]]}, "steps": 20, "evaluation_steps": 0}
        with patch("rlworkbench.engines.execute", side_effect=fixed):
            core.run(lock, self.root/"min")
        result = compare(self.root/"min", p["arms"][1]["id"], p["arms"][0]["id"], repetitions=100)
        self.assertTrue(all(e["mean_improvement"] == 3 for e in result["environments"]))

    def test_next_never_runs_and_confirmation_uses_reserved_seeds(self):
        p = protocol()
        decision = {"parent_study_id": p["study_id"], "action": "confirm", "rationale": "preselected independently", "evidence": ["development report"], "selected_arms": [a["id"] for a in p["arms"]]}
        with self.assertRaises(core.ProtocolError):
            core.next_protocol(core.freeze(p), decision, "confirm-v2")
        p["purpose"] = "development"
        new = core.next_protocol(core.freeze(p), decision, "confirm-v2")
        self.assertEqual(new["seeds"], p["holdout_seeds"])
        self.assertEqual(new["holdout_seeds"], [])
        self.assertEqual(core.validate(new), [])
        new["arms"][0]["config"]["epsilon"] = 0.7
        self.assertTrue(core.validate(new))
        new = core.next_protocol(core.freeze(p), decision, "confirm-v3")
        new["seeds"] = p["seeds"]
        self.assertTrue(core.validate(new))
        decision["action"] = "stop"
        with self.assertRaises(core.ProtocolError):
            core.next_protocol(core.freeze(p), decision, "v3")

    def test_external_import_complete_bound_raw_population(self):
        lock = core.freeze(protocol(), external=True)
        source = self.root / "external"
        for job in lock["jobs"]:
            directory = source/job["job_id"]
            core.write_new(directory/"producer.json", {"source_revision": "abc", "dependency_lock": "lockfile", "invocation": "python train.py"})
            core.write_new(directory/"result.json", {"job_id": job["job_id"], "lock_sha256": lock["lock_sha256"], "status": "completed", "metrics": {"mean_reward": 0.5}, "steps": 20, "evaluation_steps": 0})
            (directory/"raw.jsonl").write_text('{"test_fixture": true}\n')
            core.write_new(directory/"train/result.json", {"nested_raw_artifact": True})
        result = core.import_results(lock, source, self.root/"imported")
        self.assertTrue(result["population_complete"])
        self.assertTrue((self.root/"imported/jobs"/lock["jobs"][0]["job_id"]/"train/result.json").exists())
        # This validates packaging only; a raw fixture is not certified scientific data.
        (source/"unexpected").mkdir()
        with self.assertRaises(core.ProtocolError):
            core.import_results(lock, source, self.root/"bad-import")

    def test_json_duplicate_keys_and_nan_rejected(self):
        for text in ('{"x":1,"x":2}', '{"x":NaN}'):
            p = self.root/"bad.json"
            p.write_text(text)
            with self.assertRaises(core.ProtocolError):
                core.load(p)

    def test_nonobject_receipt_is_invalid_instead_of_crashing_audit(self):
        lock = core.freeze(protocol())
        out = self.root/"nonobject"
        core.run(lock, out)
        (out/"jobs"/lock["jobs"][0]["job_id"]/"result.json").write_text("[]")
        data = core.audit(out)
        self.assertEqual(data["counts"]["invalid"], 1)
        self.assertFalse(data["population_complete"])

    def test_external_eval_cannot_be_zero_or_incomplete(self):
        p = core.load(core.ROOT/"profiles/classic.json")
        p["budget"]["eval_episodes"] = 9999
        self.assertTrue(core.validate(p, native=False))
        p = core.load(core.ROOT/"profiles/classic.json")
        job = core.plan(p)[0]
        r = {"status": "completed", "steps": job["budget"]["steps"], "evaluation_steps": 0, "metrics": {"evaluation_return": 123}, "diagnostics": {"evaluation_episodes": job["budget"]["eval_episodes"]}}
        with self.assertRaises(core.ProtocolError):
            core.check_measurements(r, job, "evaluation_return")

    def test_proposed_adapter_cannot_be_frozen(self):
        p = protocol()
        p["input_adapter_ready"] = False
        self.assertEqual(core.validate(p, native=False), [])
        with self.assertRaises(core.ProtocolError):
            core.freeze(p, external=True)


if __name__ == "__main__":
    unittest.main()
