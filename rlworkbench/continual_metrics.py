"""Offline diagnostics for one lifetime; change labels are never policy inputs.

Rewards must be individual, ordered, raw training rewards. ``changes`` uses
zero-based first-post-change reward indices, not episode indices. Windows and
segments are correlated observations within ONE independent lifetime.
"""
from __future__ import annotations

import math


def summarize(rewards, changes, *, window, baseline_window=None, tolerance=0.0,
              persistence=1, direction="maximize", planned_steps=None,
              end_reason="completed", same_reward_scale=True):
    """Return raw lifetime/segment totals and pre-change-anchored recovery.

    Recovery requires ``persistence`` consecutive stride-one rolling windows,
    each wholly after the change. Confirmation is recorded at the END of the
    last qualifying window, never retroactively at the beginning of a window.
    Threshold = pre-change mean +/- absolute tolerance in raw reward units.
    A comparable reward scale does not guarantee an attainable threshold.

    ``not_recovered`` means the prespecified segment was fully observed without
    confirmation. Its recovery time is still right-censored at that horizon.
    ``censored`` means administrative observation stopped before that horizon.
    ``crash`` is a competing failure, not ordinary noninformative censoring.
    Never use the observed-prefix mean as the complete lifetime primary score.
    """
    rewards, changes = list(rewards), list(changes)
    def integer(x, lower=0):
        return type(x) is int and x >= lower
    def finite(x):
        try:
            return type(x) in (int, float) and math.isfinite(x)
        except OverflowError:
            return False
    if not all(finite(x) for x in rewards):
        raise ValueError("rewards must be finite individual raw numbers")
    if not integer(window, 1) or not integer(persistence, 1):
        raise ValueError("window and persistence must be positive integers")
    baseline_window = window if baseline_window is None else baseline_window
    if not integer(baseline_window, 1):
        raise ValueError("baseline_window must be a positive integer")
    if not finite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite, nonnegative absolute reward units")
    if direction not in {"maximize", "minimize"}:
        raise ValueError("direction must be maximize or minimize")
    if end_reason not in {"completed", "censored", "crash"}:
        raise ValueError("end_reason must be completed, censored or crash")
    if type(same_reward_scale) is not bool:
        raise ValueError("same_reward_scale must be boolean")
    n = len(rewards)
    planned_steps = n if planned_steps is None else planned_steps
    if not integer(planned_steps, 1) or n > planned_steps:
        raise ValueError("planned_steps must be positive and at least observed length")
    if end_reason == "completed" and n != planned_steps:
        raise ValueError("completed requires the complete declared horizon")
    if (any(not integer(c, 1) or c >= planned_steps for c in changes)
            or changes != sorted(set(changes))):
        raise ValueError("changes must be sorted unique indices in [1, planned_steps)")
    prefix = [0.0]
    for reward in rewards:
        prefix.append(prefix[-1] + reward)
    if not all(math.isfinite(v) for v in prefix):
        raise ValueError("reward sum overflow")
    total = prefix[-1]
    complete = end_reason == "completed" and n == planned_steps
    segments, recoveries = [], []
    boundaries = [0, *changes, planned_steps]
    for start, stop in zip(boundaries, boundaries[1:]):
        count = max(0, min(stop, n) - start)
        score = prefix[min(stop, n)] - prefix[min(start, n)]
        segments.append({"start_index": start, "end_index_exclusive": stop,
                         "observed_steps": count, "reward_sum": score,
                         "observed_mean_reward": score / count if count else None,
                         "complete": n >= stop})
    for k, change in enumerate(changes):
        stop = boundaries[k + 2]
        observed_stop = min(stop, n)
        available = max(0, observed_stop - change)
        record = {"change_index": change, "segment_end_index_exclusive": stop,
                  "observed_post_change_steps": available, "baseline_mean": None,
                  "threshold": None, "first_qualifying_window_end_step": None,
                  "confirmation_step": None, "steps_after_change": None,
                  "time_is_right_censored": False, "terminal_event": None}
        if change >= n:
            record["status"] = "not_observed"
        elif not same_reward_scale:
            record["status"] = "not_comparable"
        elif change - boundaries[k] < baseline_window:
            record["status"] = "insufficient_baseline"
        else:
            baseline = (prefix[change] - prefix[change - baseline_window]) / baseline_window
            threshold = baseline - tolerance if direction == "maximize" else baseline + tolerance
            if not math.isfinite(threshold):
                raise ValueError("recovery threshold overflow")
            record.update(baseline_mean=baseline, threshold=threshold)
            streak, first_end = 0, None
            for end in range(change + window, observed_stop + 1):
                mean = (prefix[end] - prefix[end - window]) / window
                qualifies = mean >= threshold if direction == "maximize" else mean <= threshold
                if qualifies:
                    if streak == 0:
                        first_end = end
                    streak += 1
                    if streak >= persistence:
                        record.update(status="recovered", first_qualifying_window_end_step=first_end,
                                      confirmation_step=end, steps_after_change=end - change)
                        break
                else:
                    streak, first_end = 0, None
            if "status" not in record:
                if observed_stop == n and end_reason == "crash":
                    record.update(status="crash", terminal_event="algorithm_or_system_failure")
                elif observed_stop < stop:
                    record.update(status="censored", time_is_right_censored=True,
                                  terminal_event="administrative_observation_end")
                else:
                    record.update(status="not_recovered", time_is_right_censored=True,
                                  terminal_event="next_change" if stop < planned_steps else "planned_horizon")
        recoveries.append(record)
    return {"schema_version": 1, "diagnostic_only": True,
            "lifetime": {"observed_steps": n, "planned_steps": planned_steps,
                         "observed_reward_sum": total, "complete": complete,
                         "mean_reward": total / n if complete else None,
                         "observed_mean_reward": total / n if n else None,
                         "end_reason": end_reason},
            "recovery_definition": {"window": window, "stride": 1,
                "baseline_window": baseline_window, "persistence": persistence,
                "tolerance_absolute": tolerance, "direction": direction,
                "same_reward_scale": same_reward_scale,
                "change_index_origin": "zero_based_first_post_change_reward",
                "confirmation_clock": "one_based_observed_transition_count"},
            "segments": segments, "recoveries": recoveries}
