"""Small, auditable tutorial engines; these are not research benchmark results.

Only ``execute`` writes files, and only ``events.jsonl`` inside its output_dir.
The optional SB3 adapter imports its dependencies only when explicitly run.
"""
from __future__ import annotations

import hashlib
import importlib
import json
import math
import random
from pathlib import Path

SUPPORTED_ALGORITHMS = (
    "tabular_q_learning", "tabular_sarsa", "epsilon_greedy_sample_average",
    "epsilon_greedy_constant_alpha", "sb3_ppo",
)
SUPPORTED_ENVIRONMENTS = ("cliff_grid", "stationary_bandit", "switching_bandit", "CartPole-v1")
TABULAR = {"tabular_q_learning", "tabular_sarsa"}
BANDITS = {"epsilon_greedy_sample_average", "epsilon_greedy_constant_alpha"}


def _finite(value):
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return False
    try:
        return math.isfinite(value)
    except OverflowError:
        return False


def _integer(value, minimum=0):
    return isinstance(value, int) and not isinstance(value, bool) and value >= minimum


def _seed(seed, namespace):
    """Stable independent RNG streams, shared across arms with the same run seed."""
    data = f"rlworkbench-v1:{seed}:{namespace}".encode()
    return int.from_bytes(hashlib.sha256(data).digest()[:4], "big")


def validate_job(job: dict) -> list[str]:
    """Return capability/parameter errors; shared protocol validation is separate."""
    errors = []
    if not isinstance(job, dict):
        return ["job must be an object"]
    arm, env, budget = job.get("arm", {}), job.get("env", {}), job.get("budget", {})
    if not all(isinstance(x, dict) for x in (arm, env, budget)):
        return ["arm, env and budget must be objects"]
    algorithm, environment = arm.get("algorithm"), env.get("environment")
    ac, ec = arm.get("config", {}), env.get("config", {})
    if not isinstance(ac, dict) or not isinstance(ec, dict):
        return ["algorithm and environment config must be objects"]
    if algorithm not in SUPPORTED_ALGORITHMS:
        return [f"unsupported algorithm: {algorithm!r}"]
    if environment not in SUPPORTED_ENVIRONMENTS:
        return [f"unsupported environment: {environment!r}"]
    if not _integer(job.get("seed")):
        errors.append("seed must be a nonnegative integer")
    steps, eval_n, eval_max = (budget.get(k) for k in ("steps", "eval_episodes", "max_eval_steps"))
    if not _integer(steps, 1):
        errors.append("budget.steps must be a positive integer")
    if not _integer(eval_n) or not _integer(eval_max):
        errors.append("budget.eval_episodes and max_eval_steps must be nonnegative integers")

    def unknown(config, allowed, label):
        for key in sorted(set(config) - allowed):
            errors.append(f"unsupported {label} parameter: {key}")

    def real(config, key, default, low=None, high=None, low_open=False):
        value = config.get(key, default)
        valid = _finite(value)
        if valid and low is not None:
            valid = value > low if low_open else value >= low
        if valid and high is not None:
            valid = value <= high
        if not valid:
            errors.append(f"invalid {key}: {value!r}")

    if algorithm in BANDITS:
        if environment not in {"stationary_bandit", "switching_bandit"}:
            errors.append(f"{algorithm} requires a bandit environment")
        unknown(ac, {"epsilon", "initial_value"} | ({"alpha"} if algorithm.endswith("constant_alpha") else set()), "algorithm")
        real(ac, "epsilon", 0.1, 0, 1)
        real(ac, "initial_value", 0.0)
        if algorithm.endswith("constant_alpha"):
            real(ac, "alpha", 0.1, 0, 1, True)
        allowed = {"means", "reward_std"} if environment == "stationary_bandit" else {"phases", "switch_interval", "reward_std"}
        unknown(ec, allowed, "environment")
        real(ec, "reward_std", 1.0, 0)
        phases = [ec.get("means", [0.0, 1.0])] if environment == "stationary_bandit" else ec.get("phases", [[1.0, 0.0], [0.0, 1.0]])
        if (not isinstance(phases, list) or not phases or
                any(not isinstance(p, list) or len(p) < 2 or not all(_finite(v) for v in p) for p in phases)):
            errors.append("means/phases must contain finite lists of at least two arm means")
        elif len({len(p) for p in phases}) != 1:
            errors.append("all phases must have the same number of arms")
        if environment == "switching_bandit":
            if not _integer(ec.get("switch_interval", 200), 1):
                errors.append("switch_interval must be a positive integer")
            if isinstance(phases, list) and len(phases) < 2:
                errors.append("switching_bandit requires at least two phases")
        if eval_n != 0 or eval_max != 0:
            errors.append("bandit engines measure the full online lifetime; eval_episodes and max_eval_steps must be zero")
    elif algorithm in TABULAR:
        if environment != "cliff_grid":
            errors.append(f"{algorithm} requires cliff_grid")
        unknown(ac, {"alpha", "gamma", "epsilon", "initial_value"}, "algorithm")
        unknown(ec, {"rows", "cols", "max_episode_steps", "step_reward", "cliff_penalty", "goal_reward"}, "environment")
        real(ac, "alpha", 0.3, 0, 1, True)
        real(ac, "gamma", 0.99, 0, 1)
        real(ac, "epsilon", 0.1, 0, 1)
        real(ac, "initial_value", 0.0)
        for key, default, lower in (("rows", 4, 2), ("cols", 8, 3)):
            value = ec.get(key, default)
            if not _integer(value, lower) or value > 100:
                errors.append(f"{key} must be an integer in [{lower}, 100]")
        for key, default in (("step_reward", -1.0), ("cliff_penalty", -100.0), ("goal_reward", -1.0)):
            real(ec, key, default)
    else:
        if environment != "CartPole-v1":
            errors.append("sb3_ppo supports only CartPole-v1")
        unknown(ac, {"learning_rate", "n_steps", "batch_size", "n_epochs", "gamma", "gae_lambda", "clip_range", "ent_coef", "policy_width"}, "algorithm")
        unknown(ec, {"max_episode_steps"}, "environment")
        for key, default, low, high, low_open in (
            ("learning_rate", 0.0003, 0, None, True), ("gamma", 0.99, 0, 1, False),
            ("gae_lambda", 0.95, 0, 1, False), ("clip_range", 0.2, 0, 1, True),
            ("ent_coef", 0.0, 0, None, False),
        ):
            real(ac, key, default, low, high, low_open)
        for key, default, lower in (("n_steps", 64, 2), ("batch_size", 32, 2), ("n_epochs", 2, 1), ("policy_width", 32, 1)):
            if not _integer(ac.get(key, default), lower):
                errors.append(f"{key} must be an integer >= {lower}")
        rollout, batch = ac.get("n_steps", 64), ac.get("batch_size", 32)
        if _integer(rollout, 2) and _integer(batch, 2) and (batch > rollout or rollout % batch):
            errors.append("batch_size must divide n_steps exactly")
        if _integer(steps, 1) and _integer(rollout, 2) and steps % rollout:
            errors.append("budget.steps must be divisible by n_steps: no hidden rollout overshoot")
    if algorithm not in BANDITS:
        cap = ec.get("max_episode_steps", 500 if algorithm == "sb3_ppo" else 100)
        if not _integer(cap, 1):
            errors.append("max_episode_steps must be a positive integer")
        if not _integer(eval_n, 1):
            errors.append("tabular/deep jobs require at least one fixed frozen evaluation episode")
        elif _integer(cap, 1) and _integer(eval_max) and eval_max < eval_n * cap:
            errors.append("max_eval_steps must cover eval_episodes * max_episode_steps; no incomplete evaluation")
    return errors


def epsilon_greedy(values, epsilon, rng):
    if rng.random() < epsilon:
        return rng.randrange(len(values))
    best = max(values)
    return rng.choice([a for a, v in enumerate(values) if v == best])


class BanditLearner:
    """Boundary-blind learner: update receives only an action and a reward."""
    def __init__(self, n_actions, epsilon, rng, alpha=None, initial_value=0.0):
        self.values = [float(initial_value)] * n_actions
        self.counts = [0] * n_actions
        self.epsilon, self.rng, self.alpha = epsilon, rng, alpha

    def action(self):
        return epsilon_greedy(self.values, self.epsilon, self.rng)

    def update(self, action, reward):
        self.counts[action] += 1
        step_size = self.alpha if self.alpha is not None else 1 / self.counts[action]
        self.values[action] += step_size * (reward - self.values[action])


class BanditStream:
    """Exogenous potential reward vector each step; phases are diagnostic only."""
    def __init__(self, environment, config, rng):
        self.phases = [config.get("means", [0.0, 1.0])] if environment == "stationary_bandit" else config.get("phases", [[1.0, 0.0], [0.0, 1.0]])
        self.interval = config.get("switch_interval", 200)
        self.std, self.rng, self.t = config.get("reward_std", 1.0), rng, 0

    def step(self, action):
        phase = (self.t // self.interval) % len(self.phases)
        means = self.phases[phase]
        noise = [self.rng.gauss(0.0, self.std) for _ in means]
        reward = means[action] + noise[action]
        self.t += 1
        return reward, {"phase_index": phase, "selected_mean": means[action], "optimal_mean": max(means)}


class CliffGrid:
    """Deterministic episodic grid. Cliff returns to start without termination.

    The time cap is an external sampling truncation, not an MDP terminal state.
    ``step`` returns the actual final observation before any later reset.
    """
    def __init__(self, config):
        self.rows, self.cols = config.get("rows", 4), config.get("cols", 8)
        self.cap = config.get("max_episode_steps", 100)
        self.step_reward = config.get("step_reward", -1.0)
        self.cliff_penalty = config.get("cliff_penalty", -100.0)
        self.goal_reward = config.get("goal_reward", -1.0)
        self.start, self.goal = (self.rows - 1) * self.cols, self.rows * self.cols - 1
        self.reset()

    def reset(self):
        self.state, self.elapsed = self.start, 0
        return self.state

    def step(self, action):
        row, col = divmod(self.state, self.cols)
        dr, dc = ((-1, 0), (0, 1), (1, 0), (0, -1))[action]
        row, col = min(max(row + dr, 0), self.rows - 1), min(max(col + dc, 0), self.cols - 1)
        self.elapsed += 1
        cliff = row == self.rows - 1 and 0 < col < self.cols - 1
        self.state = self.start if cliff else row * self.cols + col
        terminated = self.state == self.goal
        truncated = self.elapsed >= self.cap and not terminated
        reward = self.cliff_penalty if cliff else self.goal_reward if terminated else self.step_reward
        return self.state, float(reward), terminated, truncated


def td_target(reward, gamma, next_values, terminated, next_action=None):
    """Q-learning max or Sarsa sampled bootstrap; truncation does not zero it."""
    bootstrap = max(next_values) if next_action is None else next_values[next_action]
    return float(reward) if terminated else reward + gamma * bootstrap


class EventWriter:
    def __init__(self, path):
        self.handle = path.open("x", encoding="utf-8")

    def write(self, **event):
        self.handle.write(json.dumps({"schema_version": 1, **event}, sort_keys=True, allow_nan=False) + "\n")

    def close(self):
        self.handle.close()


def _run_bandit(job, writer):
    ac, ec = job["arm"].get("config", {}), job["env"].get("config", {})
    seed, steps = job["seed"], job["budget"]["steps"]
    env = BanditStream(job["env"]["environment"], ec, random.Random(_seed(seed, "environment")))
    learner = BanditLearner(len(env.phases[0]), ac.get("epsilon", 0.1), random.Random(_seed(seed, "policy")),
                            ac.get("alpha", 0.1) if job["arm"]["algorithm"].endswith("constant_alpha") else None,
                            ac.get("initial_value", 0.0))
    total = 0.0
    for t in range(1, steps + 1):
        action = learner.action()
        reward, diagnostic = env.step(action)
        learner.update(action, reward)
        total += reward
        writer.write(type="transition", stream="train", env_step=t, learner_update=t,
                     episode=0, episode_step=t, action=action, reward=reward,
                     terminated=False, truncated=False, diagnostic=diagnostic)
    return {"metrics": {"mean_reward": total / steps}, "steps": steps, "evaluation_steps": 0,
            "episodes": 0, "diagnostics": {"training_reward_sum": total, "lifetime_steps": steps,
            "boundary_signal_to_policy": False, "resets": 0, "final_estimates": learner.values,
            "action_counts": learner.counts, "reward_rng": "exogenous potential rewards per action per step"}}


def _run_tabular(job, writer):
    ac, ec = job["arm"].get("config", {}), job["env"].get("config", {})
    alpha, gamma, epsilon = ac.get("alpha", 0.3), ac.get("gamma", 0.99), ac.get("epsilon", 0.1)
    steps, eval_n, seed = job["budget"]["steps"], job["budget"]["eval_episodes"], job["seed"]
    env, rng = CliffGrid(ec), random.Random(_seed(seed, "policy"))
    q = [[float(ac.get("initial_value", 0.0))] * 4 for _ in range(env.rows * env.cols)]
    state, episode, total, ep_return = env.reset(), 0, 0.0, 0.0
    returns = []
    action = epsilon_greedy(q[state], epsilon, rng)
    for t in range(1, steps + 1):
        next_state, reward, terminated, truncated = env.step(action)
        next_action = epsilon_greedy(q[next_state], epsilon, rng) if not terminated else None
        target = td_target(reward, gamma, q[next_state], terminated,
                           next_action if job["arm"]["algorithm"] == "tabular_sarsa" else None)
        q[state][action] += alpha * (target - q[state][action])
        total, ep_return = total + reward, ep_return + reward
        writer.write(type="transition", stream="train", env_step=t, learner_update=t,
                     episode=episode, episode_step=env.elapsed, observation=state,
                     action=action, reward=reward, next_observation=next_state,
                     terminated=terminated, truncated=truncated,
                     bootstrap_mask=0 if terminated else 1, td_target=target)
        if terminated or truncated:
            returns.append(ep_return)
            episode, ep_return = episode + 1, 0.0
            state = env.reset()
            action = epsilon_greedy(q[state], epsilon, rng)
        else:
            state, action = next_state, next_action
    frozen_q = [row[:] for row in q]
    eval_env, eval_rng, eval_returns, eval_steps = CliffGrid(ec), random.Random(_seed(seed, "evaluation_policy")), [], 0
    for ep in range(eval_n):
        state, score = eval_env.reset(), 0.0
        while True:
            action = epsilon_greedy(q[state], 0.0, eval_rng)
            next_state, reward, terminated, truncated = eval_env.step(action)
            score, eval_steps = score + reward, eval_steps + 1
            writer.write(type="transition", stream="evaluation", env_step=eval_steps, training_env_step=steps,
                         learner_update=steps, episode=ep, episode_step=eval_env.elapsed,
                         observation=state, action=action, reward=reward, next_observation=next_state,
                         terminated=terminated, truncated=truncated)
            state = next_state
            if terminated or truncated:
                break
        eval_returns.append(score)
    assert q == frozen_q, "frozen evaluation mutated the value table"
    metrics = {"mean_reward": total / steps, "evaluation_return": sum(eval_returns) / eval_n}
    if returns:
        metrics["mean_episode_return"] = sum(returns) / len(returns)
    return {"metrics": metrics, "steps": steps, "evaluation_steps": eval_steps, "episodes": episode,
            "diagnostics": {"training_reward_sum": total, "completed_episode_returns": returns,
            "incomplete_episode_return": ep_return, "evaluation_episode_returns": eval_returns,
            "evaluation_episodes": eval_n, "evaluation_frozen": True, "bootstrap_on_truncation": True,
            "final_q": q}}


def _optional_dependencies():
    try:
        return tuple(importlib.import_module(name) for name in ("gymnasium", "stable_baselines3", "torch"))
    except ImportError as error:
        raise RuntimeError("sb3_ppo requires optional dependencies; install examples/deep-requirements.txt into a separate environment") from error


def _run_ppo(job, writer):
    gym, sb3, torch = _optional_dependencies()
    ac, ec = job["arm"].get("config", {}), job["env"].get("config", {})
    steps, seed = job["budget"]["steps"], job["seed"]
    cap, eval_n = ec.get("max_episode_steps", 500), job["budget"]["eval_episodes"]
    training_returns, evaluation_returns = [], []
    counters = {"steps": 0, "episode": 0, "episode_step": 0, "sum": 0.0, "partial": 0.0}

    class RawRewardLogger(gym.Wrapper):
        def step(self, action):
            observation, reward, terminated, truncated, info = self.env.step(action)
            counters["steps"] += 1
            counters["episode_step"] += 1
            counters["sum"] += float(reward)
            counters["partial"] += float(reward)
            writer.write(type="transition", stream="train", env_step=counters["steps"],
                         learner_update=(counters["steps"] - 1) // ac.get("n_steps", 64),
                         episode=counters["episode"], episode_step=counters["episode_step"],
                         action=int(action), reward=float(reward), terminated=bool(terminated), truncated=bool(truncated))
            if terminated or truncated:
                training_returns.append(counters["partial"])
                counters["episode"] += 1
                counters["episode_step"], counters["partial"] = 0, 0.0
            return observation, reward, terminated, truncated, info

    train_env = RawRewardLogger(gym.make("CartPole-v1", max_episode_steps=cap))
    eval_env, prior_threads = None, torch.get_num_threads()
    try:
        torch.set_num_threads(1)
        kwargs = {k: ac.get(k, default) for k, default in {
            "learning_rate": 0.0003, "n_steps": 64, "batch_size": 32, "n_epochs": 2,
            "gamma": 0.99, "gae_lambda": 0.95, "clip_range": 0.2, "ent_coef": 0.0}.items()}
        model = sb3.PPO("MlpPolicy", train_env, seed=_seed(seed, "deep_training"), device="cpu", verbose=0,
                        policy_kwargs={"net_arch": [ac.get("policy_width", 32)] * 2}, **kwargs)
        model.learn(total_timesteps=steps)
        if counters["steps"] != steps or model.num_timesteps != steps:
            raise RuntimeError("PPO training exceeded or missed the declared environment step budget")
        model.policy.set_training_mode(False)
        frozen = {name: value.detach().clone() for name, value in model.policy.state_dict().items()}
        eval_env, eval_steps = gym.make("CartPole-v1", max_episode_steps=cap), 0
        for ep in range(eval_n):
            observation, _ = eval_env.reset(seed=_seed(seed, f"evaluation_environment:{ep}"))
            score, ep_step = 0.0, 0
            while True:
                action, _ = model.predict(observation, deterministic=True)
                observation, reward, terminated, truncated, _ = eval_env.step(int(action))
                eval_steps, ep_step, score = eval_steps + 1, ep_step + 1, score + float(reward)
                writer.write(type="transition", stream="evaluation", env_step=eval_steps, training_env_step=steps,
                             learner_update=steps // ac.get("n_steps", 64), episode=ep, episode_step=ep_step,
                             action=int(action), reward=float(reward), terminated=bool(terminated), truncated=bool(truncated))
                if terminated or truncated:
                    break
            evaluation_returns.append(score)
        if not all(torch.equal(value, frozen[name]) for name, value in model.policy.state_dict().items()):
            raise RuntimeError("evaluation mutated the policy parameters or buffers")
        metrics = {"mean_reward": counters["sum"] / steps, "evaluation_return": sum(evaluation_returns) / eval_n}
        if training_returns:
            metrics["mean_episode_return"] = sum(training_returns) / len(training_returns)
        return {"metrics": metrics, "steps": steps, "evaluation_steps": eval_steps,
                "episodes": counters["episode"], "diagnostics": {
                "training_reward_sum": counters["sum"], "incomplete_episode_return": counters["partial"],
                "evaluation_episode_returns": evaluation_returns, "evaluation_episodes": eval_n,
                "evaluation_frozen": True, "evaluation_deterministic_actions": True,
                "rollouts": steps // ac.get("n_steps", 64), "learner_update_clock": "completed rollout training phases",
                "device": "cpu", "torch_num_threads": 1,
                "versions": {"gymnasium": gym.__version__, "stable_baselines3": sb3.__version__, "torch": torch.__version__}}}
    finally:
        train_env.close()
        if eval_env is not None:
            eval_env.close()
        torch.set_num_threads(prior_threads)


def execute(job: dict, output_dir: Path) -> dict:
    """Execute one validated run; refuses to overwrite its raw event record."""
    errors = validate_job(job)
    if errors:
        raise ValueError("; ".join(errors))
    writer = EventWriter(Path(output_dir) / "events.jsonl")
    try:
        algorithm = job["arm"]["algorithm"]
        result = (_run_bandit(job, writer) if algorithm in BANDITS else
                  _run_tabular(job, writer) if algorithm in TABULAR else _run_ppo(job, writer))
        json.dumps(result, allow_nan=False)
        return result
    finally:
        writer.close()
