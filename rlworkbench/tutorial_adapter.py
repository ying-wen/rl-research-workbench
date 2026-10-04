"""Tutorial META/run producer for the existing external-result workflow.

This executes trusted local Python modules, not uploaded arbitrary code. It
freezes source identities before training and preserves every planned failure.
"""
from __future__ import annotations

import argparse
import csv
import importlib
import json
import sys
from pathlib import Path

from . import core


def tutorial_runtime(root):
    """Load the explicit checkout; refuse silently mixing two checkouts."""
    root = Path(root).resolve()
    package = sys.modules.get("implementations")
    if package is not None and Path(package.__file__).resolve().parent != root / "implementations":
        raise core.ProtocolError("another tutorial checkout is loaded; start a new Python process")
    sys.path.insert(0, str(root))
    runtime = importlib.import_module("implementations.runtime")
    if Path(runtime.__file__).resolve().parent != root / "implementations":
        raise core.ProtocolError("runtime did not come from requested tutorial checkout")
    return runtime


def comparison_key(meta):
    """Metric names alone cannot make different tasks/clocks comparable."""
    required = ("id", "family", "task", "metric", "unit", "higher_better", "scope", "sources", "budget")
    missing = [key for key in required if key not in meta]
    if missing:
        raise core.ProtocolError("META missing " + ", ".join(missing))
    if type(meta["higher_better"]) is not bool:
        raise core.ProtocolError("META.higher_better must be boolean")
    return core.digest({key: meta[key] for key in ("family", "task", "metric", "unit", "higher_better", "budget")})


def make_protocol(runtime, ids, *, study_id, seeds, holdout_seeds, steps, baseline, failure_score):
    """Draft a smoke protocol; selection/failure score remain human choices."""
    if not ids or len(ids) != len(set(ids)) or baseline not in ids:
        raise core.ProtocolError("distinct algorithms and an included baseline are required")
    modules = {identifier: runtime.load(identifier) for identifier in ids}
    metas = {identifier: module.META for identifier, module in modules.items()}
    first = metas[ids[0]]
    key = comparison_key(first)
    for identifier, meta in metas.items():
        if meta["id"] != identifier or comparison_key(meta) != key:
            raise core.ProtocolError("incompatible task/metric/unit/budget: " + identifier)
    sources = sorted({source for meta in metas.values() for source in meta["sources"]})
    protocol = {
        "schema_version": 1, "study_id": study_id, "track": first["family"], "purpose": "smoke",
        "question": "Does the tutorial comparison execute and preserve its complete planned population?",
        "hypothesis": "The registered tutorial implementations produce auditable measurements; this smoke is not an efficacy test.",
        "primary_metric": first["metric"], "direction": "maximize" if first["higher_better"] else "minimize",
        "minimum_effect": 0.0, "seeds": seeds, "holdout_seeds": holdout_seeds,
        "selection": {"mode": "preselected", "uses": "development_only", "rule": "Fixed tutorial defaults; do not select a winner from this smoke."},
        "failure_policy": {"mode": "score_floor", "score_floor": failure_score}, "baseline_ids": [baseline],
        "arms": [{"id": identifier, "algorithm": "tutorial_" + identifier, "config": {"tutorial_id": identifier, "meta_sha256": core.digest(meta)}} for identifier, meta in metas.items()],
        "envs": [{"id": "tutorial_task", "environment": "tutorial_embedded", "config": {"task": first["task"], "unit": first["unit"], "budget": first["budget"]}}],
        "budget": {"steps": steps, "eval_episodes": 0, "max_eval_steps": 0, "max_total_steps": steps * len(ids) * len(seeds)},
        "provenance": {"sources": sources}, "input_adapter_ready": True,
        "checks": {"implementation": ["META identity and full tutorial source manifest are bound before execution."],
                   "mechanism": ["Only matching task, metric, unit, direction and declared budget are compared."],
                   "performance": ["Last recorded metric follows META; internal evaluation and resource costs remain tutorial-defined. Smoke does not reproduce author benchmarks."]},
        "tutorial_adapter": {"version": 1, "source_hashes": runtime.source_hashes(), "metadata": metas,
                             "aggregation": "last_recorded_value", "clock": "tutorial run(seed, steps) clock; see META.budget"},
    }
    errors = core.validate(protocol, native=False)
    if errors:
        raise core.ProtocolError("; ".join(errors))
    return protocol


def produce(lock, runtime, out):
    """Produce exactly the external lock's jobs; never overwrite an attempt."""
    core.verify_lock(lock, current_source=True)
    if lock["execution"] != "external":
        raise core.ProtocolError("tutorial producer requires freeze --external")
    adapter = lock["protocol"].get("tutorial_adapter", {})
    if adapter.get("version") != 1 or adapter.get("source_hashes") != runtime.source_hashes():
        raise core.ProtocolError("tutorial source changed after protocol creation; make a new version")
    if lock["runtime_versions"] != {k: v for k, v in core.runtime().items() if k != "platform"}:
        raise core.ProtocolError("Python/package versions changed after freeze")
    modules = {}
    for job in lock["jobs"]:
        identifier = job["arm"]["config"]["tutorial_id"]
        module = runtime.load(identifier)
        if module.META != adapter["metadata"].get(identifier) or core.digest(module.META) != job["arm"]["config"]["meta_sha256"]:
            raise core.ProtocolError("tutorial META drift: " + identifier)
        modules[identifier] = module
        if job["budget"]["eval_episodes"] != 0 or job["budget"]["max_eval_steps"] != 0:
            raise core.ProtocolError("adapter does not add external evaluation episodes")
        expected_env = {"task": module.META["task"], "unit": module.META["unit"], "budget": module.META["budget"]}
        if job["env"]["environment"] != "tutorial_embedded" or job["env"]["config"] != expected_env:
            raise core.ProtocolError("locked environment differs from embedded tutorial task")
        if set(job["arm"]["config"]) != {"tutorial_id", "meta_sha256"}:
            raise core.ProtocolError("tutorial run supports its fixed META defaults, not ignored config overrides")
    if len({comparison_key(module.META) for module in modules.values()}) != 1:
        raise core.ProtocolError("locked algorithms are not comparable")
    out = Path(out)
    out.mkdir(parents=True, exist_ok=False)
    statuses = []
    for job in lock["jobs"]:
        identifier = job["arm"]["config"]["tutorial_id"]
        module, directory = modules[identifier], out / job["job_id"]
        directory.mkdir()
        core.write_new(directory / "config.json", {"job": job, "meta": module.META, "adapter": adapter})
        versions = core.runtime()
        core.write_new(directory / "dependencies.json", versions)
        core.write_new(directory / "producer.json", {
            "source_revision": "tutorial source manifest SHA256 " + core.digest(adapter["source_hashes"]),
            "dependency_lock": "dependencies.json SHA256 " + core.digest(versions),
            "invocation": f"implementations.runtime.load({identifier!r}).run(seed={job['seed']}, steps={job['budget']['steps']}, emit=writer)",
            "identity": "independent tutorial teaching implementation; see META.scope", "source_hashes": adapter["source_hashes"],
        })
        rows = []
        result = {"job_id": job["job_id"], "lock_sha256": lock["lock_sha256"], "steps": None,
                  "evaluation_steps": 0, "diagnostics": {"evaluation_episodes": 0, "evaluation_scope": "Internal tutorial evaluation is defined in META; no additional Workbench evaluation."}}
        with (directory / "events.jsonl").open("x", encoding="utf-8") as events:
            def emit(row):
                if not isinstance(row, dict) or not core.integer(row.get("step")) or not core.finite(row.get("value")) or not isinstance(row.get("phase"), str):
                    raise core.ProtocolError("tutorial row needs finite value, integer step and phase")
                if row["step"] > job["budget"]["steps"] or (rows and row["step"] <= rows[-1]["step"]):
                    raise core.ProtocolError("tutorial clock must increase within registered horizon")
                events.write(json.dumps(row, ensure_ascii=False, allow_nan=False) + "\n")
                events.flush()
                rows.append(dict(row))
            try:
                returned = module.run(seed=job["seed"], steps=job["budget"]["steps"], emit=emit)
                # Some implementations return records but do not stream; use one representation.
                if not rows:
                    for row in returned:
                        emit(row)
                elif returned is not None and list(returned) != rows:
                    raise core.ProtocolError("returned records differ from emitted records")
                if not rows or rows[-1]["step"] != job["budget"]["steps"]:
                    raise core.ProtocolError("tutorial run did not reach registered horizon")
                result.update(status="completed", steps=rows[-1]["step"], metrics={lock["protocol"]["primary_metric"]: rows[-1]["value"]})
                core.check_measurements(result, job, lock["protocol"]["primary_metric"])
            except Exception as exc:
                result.update(status="failed", steps=rows[-1]["step"] if rows else None,
                              failure={"type": type(exc).__name__, "message": str(exc), "counts": "step is last observed tutorial clock; unknown work after last emission is not recorded as zero"})
        with (directory / "metrics.csv").open("x", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["step", "value", "phase"])
            writer.writeheader()
            writer.writerows({key: row[key] for key in writer.fieldnames} for row in rows)
        core.write_new(directory / "result.json", result)
        statuses.append({"job_id": job["job_id"], "status": result["status"]})
    return {"incoming": str(out), "jobs": statuses, "note": "Import with the existing import-results command; failures remain in the population."}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    plan = sub.add_parser("plan", help="draft an external smoke protocol without training")
    plan.add_argument("--tutorial-root", type=Path, required=True)
    plan.add_argument("--ids", nargs="+", required=True)
    plan.add_argument("--baseline", required=True)
    plan.add_argument("--study-id", required=True)
    plan.add_argument("--seeds", nargs="+", type=int, required=True)
    plan.add_argument("--holdout-seeds", nargs="+", type=int, required=True)
    plan.add_argument("--steps", type=int, required=True)
    plan.add_argument("--failure-score", type=float, required=True)
    plan.add_argument("--out", type=Path, required=True)
    run = sub.add_parser("run", help="produce every job in an already frozen external protocol")
    run.add_argument("lock", type=Path)
    run.add_argument("--tutorial-root", type=Path, required=True)
    run.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        runtime = tutorial_runtime(args.tutorial_root)
        if args.command == "plan":
            value = make_protocol(runtime, args.ids, study_id=args.study_id, seeds=args.seeds,
                                  holdout_seeds=args.holdout_seeds, steps=args.steps, baseline=args.baseline, failure_score=args.failure_score)
            core.write_new(args.out, value)
            result = {"protocol": str(args.out), "jobs": len(core.plan(value)), "purpose": "smoke"}
        else:
            result = produce(core.load(args.lock), runtime, args.out)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (core.ProtocolError, OSError, ImportError) as exc:
        parser.exit(1, str(exc) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
