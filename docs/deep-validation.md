# Optional deep adapter validation / 深度适配器验证

**Status: implementation smoke verified on 2026-10-03. No algorithm efficacy claim.**

The optional adapter is `sb3_ppo` on `CartPole-v1`. It executes Stable Baselines3 PPO; it is not a new PPO implementation. The tiny configurations in `profiles/deep.json` check execution, measurement and evidence plumbing. They do not establish a learning-rate advantage or competitive CartPole performance.

## Verified environment

| Component | Observed version / setting |
|---|---|
| Python | 3.9.6 |
| Stable Baselines3 | 2.7.1 |
| Gymnasium | 1.1.1 |
| PyTorch | 2.8.0 |
| NumPy | 1.26.2 |
| Platform | macOS 26.5, arm64 |
| Compute | CPU; one PyTorch intra-op thread during each run |

The development verification used a dedicated `.venv-deep` with `--system-site-packages` to reuse already-installed PyTorch and NumPy. SB3 and Gymnasium were installed into that virtual environment. No global packages or prior research project environments were modified. This reuse is convenient but is **not** a hermetic environment lock: use a clean virtual environment/container and retain resolved dependency versions and hashes for a research study.

`examples/deep-requirements.txt` pins the tested SB3/Gymnasium versions. It is not a complete transitive-dependency lock or a claim of universal cross-platform bitwise reproduction.

## Reproduce the optional integration check

From the repository root, use a supported Python interpreter:

```bash
python3 -m venv .venv-deep
.venv-deep/bin/python -m pip install -r examples/deep-requirements.txt
RLWORKBENCH_TEST_DEEP=1 .venv-deep/bin/python -m unittest discover -s tests -p test_engines.py -v
```

The deep test is skipped during default standard-library tests. Explicitly enabling it without installing the optional dependencies fails with an actionable installation message; there is no silent fallback to a different algorithm. The deep protocol can then follow the same `validate → freeze → run → audit → report` route as the other profiles, using this interpreter. Consult `python -m rlworkbench --help` for the exact command arguments.

## Observed smoke execution

The complete `profiles/deep.json` matrix ran through `engines.execute`. This was a **direct-adapter validation**, separate from a frozen confirmatory study. Both configurations were declared in the profile before execution. No configuration or checkpoint was selected from these observations.

| Arm | Seed | Training transitions | Evaluation transitions | Completed evaluation episodes |
|---|---:|---:|---:|---:|
| `ppo_default_lr` | 11 | 256 | 103 | 2 |
| `ppo_default_lr` | 23 | 256 | 168 | 2 |
| `ppo_lower_lr` | 11 | 256 | 100 | 2 |
| `ppo_lower_lr` | 23 | 256 | 139 | 2 |

Each training run consisted of four 64-step rollouts. Batch size 32 divided each rollout exactly. `CartPole-v1` used an explicitly overridden 100-step episode limit, rather than its standard 500-step limit. Every evaluation episode finished by termination or its declared time cap; evaluation was never silently cut off by an exhausted aggregate budget. The maximum evaluation budget was 200 transitions per job.

Checks completed:

- All training and evaluation transition counts reconciled with individual raw reward events.
- Raw training rewards were logged in a Gymnasium wrapper before SB3's timeout bootstrapping adjustment to the rollout reward.
- Evaluation used a new environment, independently derived reset seeds, deterministic actions and no learning updates.
- Policy parameters and buffers were equal before and after evaluation.
- Repeating the first matrix job in the same environment reproduced both its metrics and its complete raw event file byte for byte.
- The original PyTorch thread count was restored after execution.
- All 17 engine tests, including the opt-in real PPO integration test, passed in the verified environment.

The additional repeat and unit-test runs are validation work, outside the four-job profile budget. A future research study must account for its full development and validation cost separately from its locked run matrix.

Raw local validation records were retained under `artifacts/deep-smoke-2026-10-03/`. That directory is a local generated artifact, not required source for another user's clone. The table above records the bounded verification result; it is not an imported benchmark or published efficacy result.

## Measurement caveats

CartPole gives a reward of one per interaction, so training `mean_reward` is uninformative about policy quality at a fixed step budget. The deep profile therefore uses fixed frozen `evaluation_return` as its primary metric. Completed training-episode returns are supplementary and exclude any unfinished final training episode, whose partial return remains in diagnostics.

The `learner_update` event clock denotes completed rollout training phases for this PPO adapter, and individual TD/value updates for the standard-library adapters. It is not a cross-algorithm compute-equivalence measure. Report optimizer steps, epochs, compute time and memory separately for substantive algorithm comparisons.

Only CartPole is implemented by this adapter. Adding Atari, continuous control, recurrent policies, normalization or replay requires a new explicit adapter contract, corresponding tests and protocol metadata; changing an environment string alone is not supported.

## Primary implementation references

- [Stable Baselines3 PPO documentation](https://stable-baselines3.readthedocs.io/en/master/modules/ppo.html): rollout/minibatch parameters, CPU use and implementation differences from the original paper. The live documentation may describe a newer release than the tested pin.
- [Gymnasium time-limit semantics](https://gymnasium.farama.org/tutorials/gymnasium_basics/handling_time_limits/): distinguish termination from truncation for bootstrapping.
- [Gymnasium CartPole](https://gymnasium.farama.org/environments/classic_control/cart_pole/): environment definition and standard time limit.
