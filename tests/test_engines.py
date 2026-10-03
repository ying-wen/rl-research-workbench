"""Behavioral tests for the instructional adapters, not efficacy evidence."""
import copy
import inspect
import json
import math
import os
import random
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from rlworkbench.engines import (
    BanditLearner, BanditStream, CliffGrid, execute, td_target, validate_job,
)


def job(algorithm="epsilon_greedy_sample_average", environment="switching_bandit"):
    if algorithm.startswith("tabular"):
        return {"job_id": "test", "arm": {"id": "a", "algorithm": algorithm, "config": {"epsilon": 0.1}},
                "env": {"id": "e", "environment": "cliff_grid", "config": {"rows": 3, "cols": 5, "max_episode_steps": 12}},
                "seed": 17, "purpose": "smoke", "budget": {"steps": 100, "eval_episodes": 3, "max_eval_steps": 36}}
    if algorithm == "sb3_ppo":
        return {"job_id": "test", "arm": {"id": "a", "algorithm": algorithm, "config": {"n_steps": 8, "batch_size": 4, "n_epochs": 1}},
                "env": {"id": "e", "environment": "CartPole-v1", "config": {"max_episode_steps": 10}},
                "seed": 17, "purpose": "smoke", "budget": {"steps": 16, "eval_episodes": 2, "max_eval_steps": 20}}
    return {"job_id": "test", "arm": {"id": "a", "algorithm": algorithm, "config": {"epsilon": 0.1}},
            "env": {"id": "e", "environment": environment, "config": {"switch_interval": 25, "reward_std": 0.5} if environment == "switching_bandit" else {"means": [0.0, 1.0], "reward_std": 0.5}},
            "seed": 17, "purpose": "smoke", "budget": {"steps": 100, "eval_episodes": 0, "max_eval_steps": 0}}


class EngineTests(unittest.TestCase):
    def run_job(self, config):
        with tempfile.TemporaryDirectory() as directory:
            result = execute(config, Path(directory))
            events = [json.loads(line) for line in (Path(directory) / "events.jsonl").read_text().splitlines()]
            self.assertEqual([p.name for p in Path(directory).iterdir()], ["events.jsonl"])
        return result, events

    def test_sample_average_is_exact_empirical_average(self):
        learner = BanditLearner(2, 0, random.Random(1), initial_value=100)
        for reward in [2, 4, 9]:
            learner.update(0, reward)
        self.assertEqual(learner.values[0], 5.0)
        self.assertEqual(learner.counts, [3, 0])

    def test_constant_alpha_retains_recency(self):
        learner = BanditLearner(2, 0, random.Random(1), alpha=0.5)
        for reward in [2, 4]:
            learner.update(0, reward)
        self.assertEqual(learner.values[0], 2.5)

    def test_hidden_boundaries_and_no_lifetime_reset(self):
        learner_parameters = list(inspect.signature(BanditLearner.update).parameters)
        self.assertEqual(learner_parameters, ["self", "action", "reward"])
        result, events = self.run_job(job())
        self.assertEqual([events[i]["diagnostic"]["phase_index"] for i in [0, 24, 25, 49, 50, 74, 75]], [0, 0, 1, 1, 0, 0, 1])
        self.assertFalse(result["diagnostics"]["boundary_signal_to_policy"])
        self.assertEqual(result["diagnostics"]["resets"], 0)
        self.assertEqual(result["episodes"], 0)
        self.assertEqual(sum(result["diagnostics"]["action_counts"]), 100)
        self.assertTrue(all("phase_index" not in event for event in events))

    def test_potential_reward_noise_is_not_action_conditioned_rng(self):
        a = BanditStream("stationary_bandit", {"means": [0.0, 1.0]}, random.Random(11))
        b = BanditStream("stationary_bandit", {"means": [0.0, 1.0]}, random.Random(11))
        a.step(0)
        b.step(1)
        self.assertEqual(a.step(1), b.step(1))

    def test_identical_seed_reproduces_all_events(self):
        first = self.run_job(job())
        second = self.run_job(job())
        self.assertEqual(first, second)
        other = job()
        other["seed"] += 1
        self.assertNotEqual(first, self.run_job(other))

    def test_full_lifetime_aggregation_uses_every_raw_reward(self):
        for algorithm in ("epsilon_greedy_sample_average", "epsilon_greedy_constant_alpha"):
            result, events = self.run_job(job(algorithm))
            self.assertEqual(len(events), result["steps"])
            self.assertEqual(sum(e["reward"] for e in events), result["diagnostics"]["training_reward_sum"])
            self.assertEqual(sum(e["reward"] for e in events) / len(events), result["metrics"]["mean_reward"])
            self.assertEqual([e["env_step"] for e in events], list(range(1, 101)))
            self.assertTrue(all(math.isfinite(e["reward"]) for e in events))

    def test_cliff_is_nonterminal_reset_within_episode(self):
        env = CliffGrid({"rows": 3, "cols": 5, "max_episode_steps": 4})
        state, reward, terminated, truncated = env.step(1)
        self.assertEqual((state, reward, terminated, truncated), (env.start, -100.0, False, False))
        self.assertEqual(env.elapsed, 1)

    def test_external_time_limit_preserves_actual_observation_and_bootstrap(self):
        env = CliffGrid({"rows": 3, "cols": 5, "max_episode_steps": 1})
        observation, reward, terminated, truncated = env.step(0)
        self.assertNotEqual(observation, env.start)
        self.assertFalse(terminated)
        self.assertTrue(truncated)
        self.assertEqual(td_target(reward, 0.5, [2.0, 6.0], terminated), 2.0)
        self.assertEqual(td_target(reward, 0.5, [2.0, 6.0], terminated, 0), 0.0)
        self.assertEqual(td_target(reward, 0.5, [2.0, 6.0], True), -1.0)

    def test_goal_termination_has_precedence_at_time_limit(self):
        env = CliffGrid({"rows": 2, "cols": 3, "max_episode_steps": 1})
        env.state = 2  # immediately above the goal
        self.assertEqual(env.step(2), (5, -1.0, True, False))

    def test_tabular_frozen_eval_and_episode_accounting(self):
        for algorithm in ("tabular_q_learning", "tabular_sarsa"):
            result, events = self.run_job(job(algorithm))
            train = [e for e in events if e["stream"] == "train"]
            evaluation = [e for e in events if e["stream"] == "evaluation"]
            self.assertEqual(len(train), 100)
            self.assertEqual(len(evaluation), result["evaluation_steps"])
            self.assertLessEqual(len(evaluation), 36)
            self.assertEqual(sum(e["terminated"] or e["truncated"] for e in evaluation), 3)
            self.assertEqual(result["diagnostics"]["evaluation_episodes"], 3)
            self.assertTrue(result["diagnostics"]["evaluation_frozen"])
            self.assertAlmostEqual(sum(e["reward"] for e in evaluation) / 3, result["metrics"]["evaluation_return"])
            self.assertAlmostEqual(sum(result["diagnostics"]["completed_episode_returns"]) + result["diagnostics"]["incomplete_episode_return"], sum(e["reward"] for e in train))
            self.assertTrue(all(e["bootstrap_mask"] == 1 for e in train if e["truncated"]))
            self.assertTrue(all(e["learner_update"] == 100 for e in evaluation))

    def test_eval_budget_does_not_change_training(self):
        short = job("tabular_q_learning")
        long = copy.deepcopy(short)
        long["budget"].update(eval_episodes=6, max_eval_steps=72)
        a, ea = self.run_job(short)
        b, eb = self.run_job(long)
        self.assertEqual(a["diagnostics"]["final_q"], b["diagnostics"]["final_q"])
        self.assertEqual([e for e in ea if e["stream"] == "train"], [e for e in eb if e["stream"] == "train"])

    def test_refuses_to_overwrite_events(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            execute(job(), path)
            before = (path / "events.jsonl").read_bytes()
            with self.assertRaises(FileExistsError):
                execute(job(), path)
            self.assertEqual(before, (path / "events.jsonl").read_bytes())

    def test_unsupported_and_incomplete_configs_are_explicit_errors(self):
        invalid = []
        config = job(); config["arm"]["config"]["oracle_boundaries"] = True; invalid.append(config)
        config = job(); config["arm"]["algorithm"] = "made_up"; invalid.append(config)
        config = job(); config["env"]["environment"] = "cliff_grid"; invalid.append(config)
        config = job(); config["arm"]["config"]["epsilon"] = float("nan"); invalid.append(config)
        config = job(); config["seed"] = True; invalid.append(config)
        config = job(); config["env"]["config"]["phases"] = [[1, 2], [1]]; invalid.append(config)
        config = job("tabular_sarsa"); config["budget"]["max_eval_steps"] = 20; invalid.append(config)
        config = job("sb3_ppo"); config["budget"]["steps"] = 17; invalid.append(config)
        config = job("sb3_ppo"); config["arm"]["config"]["batch_size"] = 3; invalid.append(config)
        for config in invalid:
            with self.subTest(config=config):
                self.assertTrue(validate_job(config))
                with tempfile.TemporaryDirectory() as directory:
                    with self.assertRaises(ValueError):
                        execute(config, Path(directory))
                    self.assertEqual(list(Path(directory).iterdir()), [])

    def test_stdlib_engines_never_import_deep_dependencies(self):
        with patch("rlworkbench.engines.importlib.import_module", side_effect=AssertionError("unexpected import")):
            self.run_job(job())
            self.run_job(job("tabular_q_learning"))

    def test_missing_optional_dependencies_fail_with_actionable_message(self):
        with patch("rlworkbench.engines.importlib.import_module", side_effect=ImportError("missing")):
            with tempfile.TemporaryDirectory() as directory:
                with self.assertRaisesRegex(RuntimeError, "examples/deep-requirements.txt"):
                    execute(job("sb3_ppo"), Path(directory))

    def test_shipped_profiles_compatible(self):
        root = Path(__file__).resolve().parents[1]
        for profile_name in ("classic", "continual", "deep"):
            profile = json.loads((root / "profiles" / f"{profile_name}.json").read_text())
            self.assertEqual(profile["purpose"], "smoke")
            count = len(profile["arms"]) * len(profile["envs"]) * len(profile["seeds"])
            self.assertGreaterEqual(profile["budget"]["max_total_steps"], count * (profile["budget"]["steps"] + profile["budget"]["max_eval_steps"]))
            for arm in profile["arms"]:
                for env in profile["envs"]:
                    self.assertEqual(validate_job({"arm": arm, "env": env, "seed": profile["seeds"][0], "budget": profile["budget"]}), [])

    @unittest.skipUnless(os.environ.get("RLWORKBENCH_TEST_DEEP") == "1", "optional PPO integration; set RLWORKBENCH_TEST_DEEP=1")
    def test_real_optional_ppo_budget_and_frozen_evaluation(self):
        result, events = self.run_job(job("sb3_ppo"))
        self.assertEqual(result["steps"], 16)
        self.assertEqual(sum(e["stream"] == "train" for e in events), 16)
        self.assertEqual(sum(e["stream"] == "evaluation" for e in events), result["evaluation_steps"])
        self.assertEqual(sum(e["terminated"] or e["truncated"] for e in events if e["stream"] == "evaluation"), 2)
        self.assertLessEqual(result["evaluation_steps"], 20)
        self.assertEqual(result["diagnostics"]["rollouts"], 2)
        self.assertTrue(result["diagnostics"]["evaluation_frozen"])
        self.assertEqual(result["diagnostics"]["device"], "cpu")


if __name__ == "__main__":
    unittest.main()
