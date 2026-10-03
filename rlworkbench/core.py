"""Protocol validation, content-bound plans, and complete-population receipts.

Hashes detect accidental drift; they are not signatures or remote attestation.
External algorithms remain the producer's responsibility. No subprocess runner.
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
import platform
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IDENTIFIER = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_-]{0,79}$")


class ProtocolError(ValueError):
    pass


def canonical(obj):
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, allow_nan=False, separators=(",", ":")).encode()


def digest(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()


def file_digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def load(path):
    def invalid(value):
        raise ProtocolError(f"Non-finite JSON number: {value}")
    def unique(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                raise ProtocolError(f"Duplicate JSON key: {key}")
            out[key] = value
        return out
    with Path(path).open(encoding="utf-8") as f:
        return json.load(f, parse_constant=invalid, object_pairs_hook=unique)


def write_new(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    with path.open("x", encoding="utf-8") as f:
        f.write(data)


def now():
    return datetime.now(timezone.utc).isoformat()


def finite(value):
    try:
        return type(value) in (int, float) and math.isfinite(value)
    except OverflowError:
        return False


def integer(value, minimum=0):
    return type(value) is int and value >= minimum


def validate(protocol, *, native=True):
    """Return actionable schema/capability errors; never coerce invalid inputs."""
    errors = []
    def require(condition, message):
        if not condition:
            errors.append(message)
    if not isinstance(protocol, dict):
        return ["protocol must be an object"]
    require(type(protocol.get("schema_version")) is int and protocol.get("schema_version") == 1, "schema_version must be 1")
    require(isinstance(protocol.get("study_id"), str) and bool(IDENTIFIER.fullmatch(protocol["study_id"])), "study_id must be a safe string identifier")
    require(protocol.get("track") in {"classic", "deep", "continual"}, "unknown track")
    require(protocol.get("purpose") in {"smoke", "development", "confirmation"}, "unknown purpose")
    for field in ("question", "hypothesis", "primary_metric"):
        require(isinstance(protocol.get(field), str) and bool(protocol.get(field, "").strip()), f"{field} is required")
    require(protocol.get("direction") in {"maximize", "minimize"}, "direction must be maximize/minimize")
    require(finite(protocol.get("minimum_effect")) and protocol.get("minimum_effect", -1) >= 0, "minimum_effect must be finite and nonnegative")
    for field in ("seeds", "holdout_seeds"):
        values = protocol.get(field)
        valid = isinstance(values, list) and all(integer(x) for x in values)
        require(valid, f"{field} must be nonnegative integer list")
        if valid:
            require(len(values) == len(set(values)), f"{field} contains duplicates")
            if field == "seeds" or protocol.get("purpose") != "confirmation":
                require(len(values) >= 2, f"{field} needs at least 2 seeds (a schema minimum, not a power recommendation)")
    if errors:
        return errors
    require(not set(protocol["seeds"]) & set(protocol["holdout_seeds"]), "development and holdout seeds overlap")
    budget = protocol.get("budget", {})
    if not isinstance(budget, dict):
        return errors + ["budget must be an object"]
    for name in ("steps", "eval_episodes", "max_eval_steps", "max_total_steps"):
        require(integer(budget.get(name), 1 if name in {"steps", "max_total_steps"} else 0), f"budget.{name} invalid")
    require((budget.get("eval_episodes", 0) == 0) == (budget.get("max_eval_steps", 0) == 0), "evaluation episodes and budget must both be zero or both positive")
    if integer(budget.get("eval_episodes")) and integer(budget.get("max_eval_steps")):
        require(budget["eval_episodes"] <= budget["max_eval_steps"], "each evaluation episode requires at least one interaction")
    selection = protocol.get("selection", {})
    require(isinstance(selection, dict) and selection.get("mode") == "preselected", "v0.1 supports preselected arms only; perform HPO in a separate registered study")
    require(isinstance(selection, dict) and selection.get("uses") == "development_only", "selection.uses must be development_only")
    require(isinstance(selection, dict) and isinstance(selection.get("rule"), str) and bool(selection.get("rule", "").strip()), "selection.rule required")
    if protocol["purpose"] == "confirmation":
        frozen = selection.get("frozen_from", {}) if isinstance(selection, dict) else {}
        require(isinstance(frozen, dict) and all(frozen.get(k) for k in ("study_id", "protocol_sha256", "decision_sha256")), "confirmation needs frozen selection provenance; use next --decision")
        if isinstance(frozen, dict):
            for field in ("arms", "envs", "seeds"):
                require(frozen.get(field + "_sha256") == digest(protocol.get(field)), f"confirmation {field} changed after selection")
            require(isinstance(frozen.get("development_seeds"), list) and not set(protocol["seeds"]) & set(frozen.get("development_seeds", [])), "confirmation overlaps parent development population")
    policy = protocol.get("failure_policy", {})
    require(isinstance(policy, dict) and policy.get("mode") == "score_floor" and finite(policy.get("score_floor")), "failure_policy needs finite score_floor (predeclared composite outcome)")
    for field in ("arms", "envs"):
        records = protocol.get(field)
        if not isinstance(records, list) or not records:
            errors.append(f"{field} must be a nonempty list")
            continue
        ids = []
        for record in records:
            if not isinstance(record, dict):
                errors.append(f"{field} entries must be objects")
                continue
            require(isinstance(record.get("id"), str) and bool(IDENTIFIER.fullmatch(record["id"])), f"invalid {field} string id")
            ids.append(record.get("id"))
            require(isinstance(record.get("config"), dict), f"{field} config must be an object")
            key = "algorithm" if field == "arms" else "environment"
            require(isinstance(record.get(key), str) and bool(record.get(key)), f"{field}.{key} required")
        require(len(ids) == len(set(str(x) for x in ids)), f"duplicate {field} id")
    if errors:
        return errors
    baselines = protocol.get("baseline_ids")
    require(isinstance(baselines, list) and bool(baselines) and all(x in {a['id'] for a in protocol['arms']} for x in baselines), "baseline_ids must reference actual arms")
    for section in ("implementation", "mechanism", "performance"):
        check = protocol.get("checks", {}).get(section) if isinstance(protocol.get("checks"), dict) else None
        require(isinstance(check, list) and bool(check) and all(isinstance(x, str) and x.strip() for x in check), f"checks.{section} required")
    sources = protocol.get("provenance", {}).get("sources") if isinstance(protocol.get("provenance"), dict) else None
    require(isinstance(sources, list) and bool(sources) and all(isinstance(x, str) and x.startswith(("https://", "http://")) for x in sources), "provenance.sources needs source links")
    jobs = plan(protocol)
    require(sum(j["budget"]["steps"] + j["budget"]["max_eval_steps"] for j in jobs) <= budget["max_total_steps"], "planned interactions exceed max_total_steps")
    require(len({j['job_id'] for j in jobs}) == len(jobs), "job ID collision; rename arms/environments")
    if native and not errors:
        from .engines import validate_job
        for job in jobs:
            errors.extend(f"{job['job_id']}: {error}" for error in validate_job(job))
            metrics = {"mean_reward"} if "epsilon_greedy" in job["arm"]["algorithm"] else {"mean_reward", "evaluation_return"}
            require(protocol["primary_metric"] in metrics, "primary_metric unsupported by native engine")
    from .contracts import validate_modules
    errors.extend(validate_modules(protocol))
    if native and "modules" in protocol:
        errors.append("module contracts describe external architectures; native tutorials do not execute these modules")
    return errors


def plan(protocol):
    return [{"job_id": f"{arm['id']}--{env['id']}--s{seed}", "arm": copy.deepcopy(arm),
             "env": copy.deepcopy(env), "seed": seed, "purpose": protocol["purpose"],
             "budget": copy.deepcopy(protocol["budget"])}
            for env in protocol["envs"] for arm in protocol["arms"] for seed in protocol["seeds"]]


def source_manifest():
    files = sorted((ROOT / "rlworkbench").glob("*.py")) + sorted((ROOT / "tests").glob("*.py")) + [ROOT / "pyproject.toml"]
    return {str(path.relative_to(ROOT)): file_digest(path) for path in files}


def freeze(protocol, *, external=False):
    errors = validate(protocol, native=not external)
    if errors:
        raise ProtocolError("\n".join(errors))
    if protocol.get("input_adapter_ready") is False:
        raise ProtocolError("proposed integration is not ready: register sources, config and adapters before freezing")
    body = {"schema_version": 1, "created_at": now(), "execution": "external" if external else "native",
            "protocol": copy.deepcopy(protocol), "protocol_sha256": digest(protocol),
            "source_files": source_manifest(), "jobs": plan(protocol)}
    body["runtime_versions"] = {k: v for k, v in runtime().items() if k != "platform"}
    body["lock_sha256"] = digest(body)
    return body


def verify_lock(lock, *, current_source=False):
    if not isinstance(lock, dict):
        raise ProtocolError("lock must be an object")
    body = {k: v for k, v in lock.items() if k != "lock_sha256"}
    if digest(body) != lock.get("lock_sha256"):
        raise ProtocolError("lock content hash mismatch")
    p = lock.get("protocol", {})
    errors = validate(p, native=lock.get("execution") == "native")
    if errors:
        raise ProtocolError("invalid locked protocol: " + "; ".join(errors))
    if digest(p) != lock.get("protocol_sha256") or plan(p) != lock.get("jobs"):
        raise ProtocolError("protocol/plan mismatch")
    if lock.get("execution") not in {"native", "external"}:
        raise ProtocolError("unknown execution mode")
    if current_source and lock.get("source_files") != source_manifest():
        raise ProtocolError("source changed after freeze; make a new study version and lock")


def runtime():
    from importlib.metadata import version, PackageNotFoundError
    versions = {}
    for name in ("numpy", "torch", "gymnasium", "stable-baselines3"):
        try:
            versions[name] = version(name)
        except PackageNotFoundError:
            pass
    return {"python": sys.version.split()[0], "platform": platform.platform(), "packages": versions}


def artifacts(directory):
    if directory.is_symlink() or any(p.is_symlink() for p in directory.rglob("*")):
        raise ProtocolError("artifact symlinks unsupported; use actual files")
    return {str(p.relative_to(directory)): file_digest(p) for p in sorted(directory.rglob("*"))
            if p.is_file() and p != directory / "result.json"}


def check_measurements(result, job, metric):
    if result.get("status") != "completed":
        raise ProtocolError("measurement validation requires completed status")
    if not integer(result.get("steps")) or result["steps"] != job["budget"]["steps"]:
        raise ProtocolError("completed result must cover exactly the registered training horizon")
    if not integer(result.get("evaluation_steps")) or result["evaluation_steps"] > job["budget"]["max_eval_steps"]:
        raise ProtocolError("invalid evaluation step count")
    if job["budget"]["eval_episodes"]:
        diagnostics = result.get("diagnostics", {})
        if not isinstance(diagnostics, dict) or type(diagnostics.get("evaluation_episodes")) is not int or diagnostics["evaluation_episodes"] != job["budget"]["eval_episodes"]:
            raise ProtocolError("evaluation episode population does not match protocol")
        if result["evaluation_steps"] < job["budget"]["eval_episodes"]:
            raise ProtocolError("evaluation steps cannot cover the registered episodes")
    metrics = result.get("metrics")
    if not isinstance(metrics, dict) or metric not in metrics or not all(finite(x) for x in metrics.values()):
        raise ProtocolError("metrics must be finite and include the primary metric")


def run(lock, out):
    verify_lock(lock, current_source=True)
    if lock["execution"] != "native":
        raise ProtocolError("external lock must use import-results")
    if lock.get("runtime_versions") != {k: v for k, v in runtime().items() if k != "platform"}:
        raise ProtocolError("Python/package versions differ from freeze; re-register for this environment")
    if any(j["arm"]["algorithm"] == "sb3_ppo" for j in lock["jobs"]):
        import importlib.util
        if any(importlib.util.find_spec(name) is None for name in ("stable_baselines3", "gymnasium")):
            raise ProtocolError("optional PPO dependencies unavailable; install examples/deep-requirements.txt in the run environment, then freeze there")
    from .engines import execute
    out = Path(out)
    out.mkdir(parents=True, exist_ok=False)  # no silent reruns or overwrite
    write_new(out / "lock.json", lock)
    write_new(out / "runtime.json", runtime())
    for job in lock["jobs"]:
        directory = out / "jobs" / job["job_id"]
        directory.mkdir(parents=True)
        started = now()
        try:
            result = execute(copy.deepcopy(job), directory)
            result["status"] = "completed"
            check_measurements(result, job, lock["protocol"]["primary_metric"])
        except Exception as exc:
            result = {"status": "failed", "failure": {"type": type(exc).__name__, "message": str(exc)},
                      "metrics": {}, "steps": None, "evaluation_steps": None,
                      "note": "Unknown counters are not replaced by zero; inspect preserved event log."}
        result.update(job_id=job["job_id"], lock_sha256=lock["lock_sha256"], started_at=started,
                      finished_at=now(), artifacts=artifacts(directory))
        result["result_sha256"] = digest(result)
        write_new(directory / "result.json", result)
    write_new(out / "finished.json", {"finished_at": now(), "planned_jobs": len(lock["jobs"]),
                                      "lock_sha256": lock["lock_sha256"]})
    return audit(out)


def audit(out):
    """Keep missing, failed, corrupt, and successful jobs distinct."""
    out = Path(out)
    lock = load(out / "lock.json")
    verify_lock(lock)
    rows = []
    for job in lock["jobs"]:
        path = out / "jobs" / job["job_id"] / "result.json"
        row = {"job_id": job["job_id"], "arm": job["arm"]["id"], "env": job["env"]["id"], "seed": job["seed"], "status": "missing"}
        if path.exists():
            try:
                result = load(path)
                if not isinstance(result, dict):
                    raise ProtocolError("receipt must be a JSON object")
                if digest({k: v for k, v in result.items() if k != "result_sha256"}) != result.get("result_sha256"):
                    raise ProtocolError("result content hash mismatch")
                if result.get("job_id") != job["job_id"] or result.get("lock_sha256") != lock["lock_sha256"]:
                    raise ProtocolError("receipt identity mismatch")
                if result.get("status") not in {"completed", "failed"}:
                    raise ProtocolError("unknown receipt status")
                if not isinstance(result.get("artifacts"), dict) or result["artifacts"] != artifacts(path.parent):
                    raise ProtocolError("artifact content/list changed")
                if result["status"] == "completed":
                    check_measurements(result, job, lock["protocol"]["primary_metric"])
                    row.update(score=result["metrics"][lock["protocol"]["primary_metric"]], steps=result["steps"], evaluation_steps=result["evaluation_steps"])
                else:
                    if not isinstance(result.get("failure"), dict):
                        raise ProtocolError("failure detail is missing")
                    row.update(score=lock["protocol"]["failure_policy"]["score_floor"], failure=result.get("failure"))
                row["status"] = result["status"]
            except (ValueError, OSError, KeyError, TypeError) as exc:
                row.update(status="invalid", error=str(exc))
        rows.append(row)
    known = {j["job_id"] for j in lock["jobs"]}
    extra = sorted(p.name for p in (out / "jobs").glob("*") if p.name not in known)
    counts = {status: sum(r["status"] == status for r in rows) for status in ("completed", "failed", "missing", "invalid")}
    return {"study_id": lock["protocol"]["study_id"], "purpose": lock["protocol"]["purpose"],
            "lock_sha256": lock["lock_sha256"], "counts": counts, "extra_jobs": extra,
            "population_complete": counts["missing"] == counts["invalid"] == 0 and not extra,
            "rows": rows, "claim_status": "workflow_smoke_only" if lock["protocol"]["purpose"] == "smoke" else "requires_scientific_review"}


def import_results(lock, source, out):
    """Ingest all pre-registered external jobs; bind copied artifacts to receipts.

    Every input job folder has result.json, producer.json and raw artifacts.
    producer.json must describe source revision, dependency lock and invocation.
    This checks evidence packaging, not whether an external scientific run is valid.
    """
    import shutil
    verify_lock(lock, current_source=True)
    if lock["execution"] != "external":
        raise ProtocolError("use freeze --external for external producers")
    source, out = Path(source), Path(out)
    if not source.is_dir() or source.resolve() == out.resolve() or source.resolve() in out.resolve().parents or out.resolve() in source.resolve().parents:
        raise ProtocolError("source and output must be separate directories")
    if out.exists():
        raise ProtocolError("output exists; never overwrite attempts")
    expected = {j['job_id'] for j in lock['jobs']}
    actual = {p.name for p in source.iterdir()}
    if actual != expected:
        raise ProtocolError(f"external population mismatch: missing={sorted(expected-actual)}, extra={sorted(actual-expected)}")
    prepared = []
    for job in lock["jobs"]:
        directory = source / job['job_id']
        if directory.is_symlink() or any(p.is_symlink() for p in directory.rglob('*')):
            raise ProtocolError("external artifact symlinks are unsupported")
        result = load(directory / "result.json")
        if not isinstance(result, dict):
            raise ProtocolError("external receipt must be a JSON object")
        if result.get("job_id") != job["job_id"] or result.get("lock_sha256") != lock["lock_sha256"]:
            raise ProtocolError("external result must bind job_id and lock_sha256")
        producer = load(directory / "producer.json")
        if not isinstance(producer, dict):
            raise ProtocolError("producer must be a JSON object")
        for field in ("source_revision", "dependency_lock", "invocation"):
            if not isinstance(producer.get(field), str) or not producer[field].strip():
                raise ProtocolError(f"producer.{field} required")
        if result.get("status") == "completed":
            check_measurements(result, job, lock["protocol"]["primary_metric"])
        elif result.get("status") != "failed" or not isinstance(result.get("failure"), dict):
            raise ProtocolError("external status must be completed/failed with failure detail")
        files = artifacts(directory)
        if not any(k not in {"producer.json"} for k in files):
            raise ProtocolError("external run needs raw evidence beyond result/producer summaries")
        prepared.append((job, result, files))
    out.mkdir(parents=True, exist_ok=False)
    write_new(out / "lock.json", lock)
    write_new(out / "runtime.json", {"importer": runtime(), "external_scientific_validation": "not_attested"})
    for job, result, hashes in prepared:
        directory = source / job['job_id']
        target = out / "jobs" / job['job_id']
        target.mkdir(parents=True)
        for name, expected_hash in hashes.items():
            p = directory / name
            dest = target / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(p, dest)
            if file_digest(dest) != expected_hash:
                raise ProtocolError("external artifact changed during copy; retain incomplete attempt")
        result = {**result, "artifacts": hashes, "imported_at": now(), "evidence_origin": "external_producer"}
        result.pop("result_sha256", None)
        result["result_sha256"] = digest(result)
        write_new(target / "result.json", result)
    write_new(out / "finished.json", {"finished_at": now(), "planned_jobs": len(lock["jobs"]), "lock_sha256": lock["lock_sha256"]})
    return audit(out)


def next_protocol(lock, decision, study_id):
    """Explicit lineage, never automatic winner selection or automatic execution."""
    verify_lock(lock)
    if not isinstance(decision, dict) or decision.get("parent_study_id") != lock["protocol"]["study_id"]:
        raise ProtocolError("decision must identify its parent study")
    if decision.get("action") not in {"continue", "revise", "confirm", "stop"}:
        raise ProtocolError("decision action must be continue/revise/confirm/stop")
    if not isinstance(decision.get("rationale"), str) or not decision["rationale"].strip():
        raise ProtocolError("decision rationale required")
    if not isinstance(decision.get("evidence"), list) or not decision["evidence"] or not all(isinstance(x, str) and x.strip() for x in decision["evidence"]):
        raise ProtocolError("decision needs evidence references (not automatically verified)")
    if decision["action"] == "stop":
        raise ProtocolError("decision stops this line; no next study generated")
    if study_id == lock["protocol"]["study_id"] or not IDENTIFIER.fullmatch(study_id):
        raise ProtocolError("next study needs a new safe study_id")
    p = copy.deepcopy(lock["protocol"])
    p["study_id"] = study_id
    p["lineage"] = {"parent_study_id": lock["protocol"]["study_id"], "parent_lock_sha256": lock["lock_sha256"],
                    "decision_sha256": digest(decision), "decision": copy.deepcopy(decision)}
    if decision["action"] == "confirm":
        if p["purpose"] == "smoke":
            raise ProtocolError("smoke cannot be promoted directly to scientific confirmation; design a development study first")
        if p["purpose"] == "confirmation" or len(p["holdout_seeds"]) < 2:
            raise ProtocolError("confirmation needs unused reserved seeds from a development study")
        ids = decision.get("selected_arms")
        all_ids = {a["id"] for a in p["arms"]}
        if not isinstance(ids, list) or len(ids) != len(set(ids)) or len(ids) < 2 or not set(ids) <= all_ids or not set(p["baseline_ids"]) <= set(ids):
            raise ProtocolError("selected_arms must retain baselines plus at least one comparison arm")
        p["arms"] = [a for a in p["arms"] if a["id"] in ids]
        p["purpose"] = "confirmation"
        p["seeds"], p["holdout_seeds"] = p["holdout_seeds"], []
        p["selection"]["frozen_from"] = {"study_id": lock["protocol"]["study_id"], "protocol_sha256": lock["protocol_sha256"], "decision_sha256": digest(decision), "arms_sha256": digest(p["arms"]), "envs_sha256": digest(p["envs"]), "seeds_sha256": digest(p["seeds"]), "development_seeds": copy.deepcopy(lock["protocol"]["seeds"])}
    else:
        p["purpose"] = "development"
        p["selection"].pop("frozen_from", None)
        if lock["protocol"]["purpose"] == "confirmation":
            raise ProtocolError("after confirmation, register a fresh development study and unused holdout population explicitly")
    return p
