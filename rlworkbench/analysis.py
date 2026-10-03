"""Transparent per-environment paired summaries; no implicit benchmark ranking."""
from __future__ import annotations

import math
import random
import statistics
from pathlib import Path

from .core import ProtocolError, audit, load


def quantile(values, q):
    values = sorted(values)
    position = (len(values) - 1) * q
    low = math.floor(position)
    high = math.ceil(position)
    return values[low] + (values[high] - values[low]) * (position - low)


def paired_interval(differences, *, repetitions=10000, confidence=0.95, seed=0):
    if len(differences) < 2:
        raise ProtocolError("need at least two paired training/lifetime seeds")
    if not isinstance(repetitions, int) or repetitions < 100 or repetitions > 1000000:
        raise ProtocolError("bootstrap repetitions must be 100..1000000")
    if not 0 < confidence < 1:
        raise ProtocolError("confidence must lie in (0,1)")
    rng = random.Random(seed)
    values = [statistics.fmean(rng.choices(differences, k=len(differences))) for _ in range(repetitions)]
    tail = (1 - confidence) / 2
    return [quantile(values, tail), quantile(values, 1 - tail)]


def compare(out, candidate, baseline, *, repetitions=10000):
    population = audit(out)
    if not population["population_complete"]:
        raise ProtocolError("comparison requires complete, valid predeclared population; missing jobs are not failure scores")
    lock = load(Path(out) / "lock.json")
    p = lock["protocol"]
    ids = {a["id"] for a in p["arms"]}
    if candidate == baseline or candidate not in ids or baseline not in p["baseline_ids"]:
        raise ProtocolError("choose a distinct candidate and a registered baseline")
    sign = 1 if p["direction"] == "maximize" else -1
    environments = []
    for env in p["envs"]:
        rows = { (r["arm"], r["seed"]): r for r in population["rows"] if r["env"] == env["id"]}
        differences = [sign * (rows[(candidate, s)]["score"] - rows[(baseline, s)]["score"]) for s in p["seeds"]]
        interval = paired_interval(differences, repetitions=repetitions)
        environments.append({"env": env["id"], "independent_unit": "paired_training_run_or_lifetime",
            "n_pairs": len(differences), "seed_ids": p["seeds"], "signed_differences": differences,
            "mean_improvement": statistics.fmean(differences), "median_improvement": statistics.median(differences),
            "sample_sd_difference": statistics.stdev(differences), "percentile_bootstrap_95_interval": interval,
            "observed_positive_pair_fraction": sum(x > 0 for x in differences)/len(differences),
            "failures": {a: sum(rows[(a, s)]["status"] == "failed" for s in p["seeds"]) for a in (candidate, baseline)},
            "minimum_effect": p["minimum_effect"], "interpretation": "descriptive_only_pending_design_review"})
    return {"study_id": p["study_id"], "purpose": p["purpose"], "candidate": candidate, "baseline": baseline,
        "metric": p["primary_metric"], "positive_means": "candidate improvement", "environments": environments,
        "bootstrap": {"repetitions": repetitions, "analysis_seed": 0, "resampled_unit": "paired seed within one fixed environment"},
        "claim_status": population["claim_status"],
        "limitations": ["Few-seed percentile bootstrap can have poor coverage; no seed-count guarantee.",
          "Same seed labels do not imply identical policy-dependent trajectories or valid coupling.",
          "Failed jobs receive the predeclared adverse score; this changes the estimand to a composite outcome.",
          "No HPO-selection correction, multiple-comparison correction, task-distribution inference or automatic promotion.",
          "Positive-pair fraction is not rliable cross-run probability of improvement."]}


def markdown_report(out):
    data = audit(out)
    p = load(Path(out) / "lock.json")["protocol"]
    lines = [f"# 实验记录 {data['study_id']}", "", f"用途：**{p['purpose']}**；证据状态：**{data['claim_status']}**。", "",
             f"问题：{p['question']}", "", f"主指标：`{p['primary_metric']}`；完整预定人口：{data['population_complete']}。", "",
             "| 环境 | 方法 | 完成 | 失败 | 缺失 | 无效 | 含预定失败分值的均值 |", "|---|---|---:|---:|---:|---:|---:|"]
    for env in p["envs"]:
        for arm in p["arms"]:
            rows = [r for r in data["rows"] if r["env"] == env["id"] and r["arm"] == arm["id"]]
            counts = [sum(r["status"] == status for r in rows) for status in ("completed", "failed", "missing", "invalid")]
            value = f"{statistics.fmean(r['score'] for r in rows):.6g}" if counts[2] == counts[3] == 0 else "不汇总未完整人口"
            lines.append(f"| {env['id']} | {arm['id']} | {' | '.join(map(str, counts))} | {value} |")
    lines += ["", "这些统计未校正多重比较或调参选择；不同环境的原始回报不直接混合。", "",
              "实现检查、机制证据与性能结论需分别审阅。短程示例不证明算法优越或持续学习能力。", "",
              "完整记录与逐步奖励位于本目录的 lock.json、runtime.json 和 jobs/；失败原样保留。", ""]
    return "\n".join(lines)
