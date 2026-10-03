"""One bounded, explicit action per command."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from . import core
from .analysis import compare, markdown_report


def parser():
    p = argparse.ArgumentParser(prog="rlwb", description="RL research protocols and small tutorial runs")
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="command", required=True)
    s = sub.add_parser("init", help="copy a small explicit starter protocol")
    s.add_argument("--profile", choices=["classic", "deep", "continual"], required=True)
    s.add_argument("--out", type=Path, required=True)
    for command in ("validate", "plan", "freeze"):
        s = sub.add_parser(command)
        s.add_argument("protocol", type=Path)
        s.add_argument("--external", action="store_true", help="use an external producer, do not claim native capability")
        if command == "freeze":
            s.add_argument("--out", type=Path, required=True)
        if command == "plan":
            s.add_argument("--summary", action="store_true", help="show population and budget without every job")
    s = sub.add_parser("run", help="run a frozen native plan in a new directory")
    s.add_argument("lock", type=Path)
    s.add_argument("--out", type=Path, required=True)
    s = sub.add_parser("import-results", help="validate and copy external complete-population receipts")
    s.add_argument("lock", type=Path)
    s.add_argument("--input", type=Path, required=True)
    s.add_argument("--out", type=Path, required=True)
    for command in ("audit", "report", "compare"):
        s = sub.add_parser(command)
        s.add_argument("run_directory", type=Path)
        if command == "report":
            s.add_argument("--out", type=Path)
        if command == "compare":
            s.add_argument("--candidate", required=True)
            s.add_argument("--baseline", required=True)
            s.add_argument("--bootstrap", type=int, default=10000)
    s = sub.add_parser("next", help="make an unfrozen next protocol from an explicit research decision")
    s.add_argument("lock", type=Path)
    s.add_argument("--decision", type=Path, required=True)
    s.add_argument("--study-id", required=True)
    s.add_argument("--out", type=Path, required=True)
    s = sub.add_parser("continual-metrics", help="offline recovery diagnostics from one raw lifetime event log")
    s.add_argument("events", type=Path)
    s.add_argument("--changes", required=True, help="comma-separated zero-based first-post-change indices")
    s.add_argument("--window", type=int, required=True)
    s.add_argument("--baseline-window", type=int)
    s.add_argument("--persistence", type=int, default=1)
    s.add_argument("--tolerance", type=float, default=0.0)
    s.add_argument("--planned-steps", type=int, required=True)
    s.add_argument("--end-reason", choices=["completed", "censored", "crash"], default="completed")
    s.add_argument("--direction", choices=["maximize", "minimize"], default="maximize")
    s.add_argument("--different-reward-scale", action="store_true")
    s = sub.add_parser("validate-modules", help="check declared module wiring without executing modules")
    s.add_argument("contract", type=Path)
    return p


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        command = args.command
        if command == "init":
            value = core.load(core.ROOT / "profiles" / (args.profile + ".json"))
            core.write_new(args.out, value)
            result = {"created": str(args.out), "purpose": value["purpose"]}
        elif command in {"validate", "plan", "freeze"}:
            p = core.load(args.protocol)
            errors = core.validate(p, native=not args.external)
            if errors:
                raise core.ProtocolError("\n".join(errors))
            if command == "freeze":
                value = core.freeze(p, external=args.external)
                core.write_new(args.out, value)
                result = {"created": str(args.out), "lock_sha256": value["lock_sha256"], "jobs": len(value["jobs"])}
            elif command == "plan":
                jobs = core.plan(p)
                result = {"study_id": p["study_id"], "jobs": jobs, "maximum_interactions": sum(j["budget"]["steps"]+j["budget"]["max_eval_steps"] for j in jobs)}
                if args.summary:
                    result["jobs"] = len(jobs)
                    result["population"] = {"arms": len(p["arms"]), "environments": len(p["envs"]), "seeds": len(p["seeds"])}
            else:
                result = {"valid": True, "mode": "external" if args.external else "native", "note": "Schema/capability validation does not certify scientific design or dependency availability."}
        elif command in {"run", "import-results"}:
            lock = core.load(args.lock)
            result = core.run(lock, args.out) if command == "run" else core.import_results(lock, args.input, args.out)
        elif command == "audit":
            result = core.audit(args.run_directory)
        elif command == "compare":
            result = compare(args.run_directory, args.candidate, args.baseline, repetitions=args.bootstrap)
        elif command == "report":
            report = markdown_report(args.run_directory)
            if args.out:
                args.out.parent.mkdir(parents=True, exist_ok=True)
                with args.out.open("x", encoding="utf-8") as f:
                    f.write(report)
                result = {"created": str(args.out)}
            else:
                print(report)
                return 0
        elif command == "next":
            result = core.next_protocol(core.load(args.lock), core.load(args.decision), args.study_id)
            core.write_new(args.out, result)
            result = {"created": str(args.out), "purpose": result["purpose"], "frozen": False,
                      "note": "Review/edit the new design, validate and freeze before running."}
        elif command == "continual-metrics":
            from .continual_metrics import summarize
            changes = [int(x.strip()) for x in args.changes.split(",") if x.strip()]
            rewards = []
            with args.events.open(encoding="utf-8") as f:
                for line in f:
                    event = json.loads(line)
                    if not isinstance(event, dict):
                        raise core.ProtocolError("events must be JSON objects")
                    # Native engines emit "train"; retain "training" for
                    # existing external producers using the documented alias.
                    if event.get("type") == "transition" and event.get("stream") in {"train", "training"}:
                        if type(event.get("env_step")) is not int or event["env_step"] != len(rewards)+1:
                            raise core.ProtocolError("training event clock must be contiguous from 1")
                        rewards.append(event["reward"])
            result = summarize(rewards, changes, window=args.window, baseline_window=args.baseline_window,
                               persistence=args.persistence, tolerance=args.tolerance, direction=args.direction,
                               planned_steps=args.planned_steps, end_reason=args.end_reason,
                               same_reward_scale=not args.different_reward_scale)
        elif command == "validate-modules":
            from .contracts import validate_modules
            errors = validate_modules(core.load(args.contract))
            if errors:
                raise core.ProtocolError("\n".join(errors))
            result = {"valid": True, "scope": "declared module structure only", "runtime_information_flow_verified": False, "modules_executed": 0}
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
        if command in {"run", "import-results", "audit"}:
            return 0 if result["population_complete"] and result["counts"]["failed"] == 0 else 1
        return 0
    except (core.ProtocolError, OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
