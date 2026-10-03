"""Validate declared module wiring; this is not runtime information-flow proof."""
from __future__ import annotations

import re

IDENTIFIER = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*$")
AVAILABILITY = {"decision_time", "after_transition", "after_update", "previous_step",
                "previous_option", "previous_lifetime", "initialization"}
DELAYED = {"previous_step", "previous_option", "previous_lifetime"}
EVIDENCE = {"proposed", "implemented", "validated"}


def validate_modules(protocol) -> list[str]:
    """Validate optional modules, references, declared privilege and clock loops.

    Internal input sources use ``module_id.output_name``. External sources use
    ``external:signal_name``. Deployment includes any module whose outputs or
    persistent updates influence future real actions, not merely the actor.
    Diagnostic taint is conservative: all outputs of a module inherit it.
    A previously observed diagnostic signal remains privileged when delayed.
    Evidence status is a declaration, not a certificate issued by this check.
    """
    if not isinstance(protocol, dict):
        return ["protocol must be an object"]
    if "modules" not in protocol:
        return []
    modules = protocol["modules"]
    if not isinstance(modules, list) or not modules:
        return ["modules must be a nonempty list when provided"]
    errors, by_id = [], {}
    def nonempty(value):
        return isinstance(value, str) and bool(value.strip())
    def strings(value, *, allow_empty=True):
        return (isinstance(value, list) and (allow_empty or bool(value))
                and all(nonempty(v) for v in value) and len(value) == len(set(value)))
    for i, module in enumerate(modules):
        if not isinstance(module, dict):
            errors.append(f"modules[{i}] must be an object")
            continue
        mid = module.get("id")
        if not isinstance(mid, str) or not IDENTIFIER.fullmatch(mid):
            errors.append(f"modules[{i}].id must be a safe identifier")
            continue
        if mid in by_id:
            errors.append(f"duplicate module id: {mid}")
        by_id[mid] = module
        for field in ("role", "update_clock", "objective", "measure"):
            if not nonempty(module.get(field)):
                errors.append(f"{mid}.{field} must be a nonempty string")
        for field in ("outputs", "persistent_state", "downstream_consumers", "costs"):
            if not strings(module.get(field), allow_empty=field in {"persistent_state", "downstream_consumers"}):
                errors.append(f"{mid}.{field} must be a list of unique nonempty strings")
        if strings(module.get("outputs")) and any(not IDENTIFIER.fullmatch(x) for x in module["outputs"]):
            errors.append(f"{mid}.outputs must use safe identifiers")
        if type(module.get("deployment")) is not bool:
            errors.append(f"{mid}.deployment must be explicitly boolean")
        if module.get("role") == "actor" and module.get("deployment") is not True:
            errors.append(f"{mid}: role actor must declare deployment=true; isolate diagnostic actors under role diagnostic")
        if not isinstance(module.get("evidence_status"), str) or module["evidence_status"] not in EVIDENCE:
            errors.append(f"{mid}.evidence_status must be proposed, implemented or validated")
        inputs = module.get("inputs")
        if not isinstance(inputs, list):
            errors.append(f"{mid}.inputs must be a list")
            continue
        names = []
        for index, item in enumerate(inputs):
            tag = f"{mid}.inputs[{index}]"
            if not isinstance(item, dict):
                errors.append(f"{tag} must be an object")
                continue
            for field in ("name", "source"):
                if not nonempty(item.get(field)):
                    errors.append(f"{tag}.{field} is required")
            names.append(item.get("name"))
            if not isinstance(item.get("available_at"), str) or item["available_at"] not in AVAILABILITY:
                errors.append(f"{tag}.available_at must declare a supported event/lag")
            if not isinstance(item.get("privilege"), str) or item["privilege"] not in {"agent", "diagnostic"}:
                errors.append(f"{tag}.privilege must be agent or diagnostic")
        if all(isinstance(x, str) for x in names) and len(names) != len(set(names)):
            errors.append(f"{mid}: duplicate input names")
    if errors:
        return errors
    adjacency = {mid: set() for mid in by_id}
    immediate = {mid: set() for mid in by_id}
    tainted = set()
    for mid, module in by_id.items():
        for item in module["inputs"]:
            source = item["source"]
            if item["privilege"] == "diagnostic":
                tainted.add(mid)
            if source.startswith("external:"):
                if not source[len("external:"):].strip():
                    errors.append(f"{mid}: external source needs a signal name")
                continue
            parts = source.split(".")
            if len(parts) != 2 or parts[0] not in by_id:
                errors.append(f"{mid}: unknown internal source {source!r}; use module.output or external:signal")
                continue
            parent, output = parts
            if output not in by_id[parent]["outputs"]:
                errors.append(f"{mid}: unknown output {source}")
            adjacency[parent].add(mid)
            if item["available_at"] not in DELAYED:
                immediate[parent].add(mid)
            if mid not in by_id[parent]["downstream_consumers"]:
                errors.append(f"{parent}: missing declared downstream consumer {mid}")
    for mid, module in by_id.items():
        for consumer in module["downstream_consumers"]:
            if consumer not in by_id:
                errors.append(f"{mid}: unknown downstream consumer {consumer}")
            elif consumer not in adjacency[mid]:
                errors.append(f"{mid}: consumer {consumer} lacks matching module-output input")
    frontier = list(tainted)
    while frontier:
        for child in adjacency[frontier.pop()]:
            if child not in tainted:
                tainted.add(child)
                frontier.append(child)
    for mid in sorted(tainted):
        if by_id[mid]["deployment"]:
            errors.append(f"{mid}: diagnostic privilege reaches a deploying module")
    # Only remove explicitly delayed edges; recurrent loops remain legal.
    visiting, visited = set(), set()
    def cycle(mid):
        if mid in visiting:
            return True
        if mid in visited:
            return False
        visiting.add(mid)
        if any(cycle(child) for child in immediate[mid]):
            return True
        visiting.remove(mid)
        visited.add(mid)
        return False
    if any(cycle(mid) for mid in by_id if mid not in visited):
        errors.append("same-cycle module dependency loop: declare actual previous-step/option/lifetime lag or redesign event ordering")
    return errors
