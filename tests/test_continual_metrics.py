import unittest
from rlworkbench.continual_metrics import summarize


class ContinualMetricTests(unittest.TestCase):
    def test_full_lifetime_and_segments_include_every_raw_reward(self):
        result = summarize([1, 2, 3, 4, 5, 6], [2, 4], window=2)
        self.assertEqual(result['lifetime']['mean_reward'], 3.5)
        self.assertEqual([s['reward_sum'] for s in result['segments']], [3, 7, 11])
        self.assertEqual(sum(s['observed_steps'] for s in result['segments']), 6)

    def test_confirmation_occurs_at_window_end_with_persistence(self):
        result = summarize([10, 10, 0, 10, 10, 10], [2], window=2, persistence=2)
        r = result['recoveries'][0]
        self.assertEqual(r['threshold'], 10)
        self.assertEqual(r['first_qualifying_window_end_step'], 5)
        self.assertEqual(r['confirmation_step'], 6)
        self.assertEqual(r['steps_after_change'], 4)

    def test_prechange_samples_cannot_fill_recovery_window(self):
        r = summarize([10, 10, 10], [2], window=2)['recoveries'][0]
        self.assertEqual(r['status'], 'not_recovered')
        self.assertIsNone(r['confirmation_step'])

    def test_absolute_threshold_handles_negative_rewards(self):
        r = summarize([-10, -10, -11, -11], [2], window=2, tolerance=1)['recoveries'][0]
        self.assertEqual(r['threshold'], -11)
        self.assertEqual(r['status'], 'recovered')

    def test_minimization_threshold(self):
        r = summarize([1, 1, 2, 2], [2], window=2, tolerance=1, direction='minimize')['recoveries'][0]
        self.assertEqual(r['status'], 'recovered')

    def test_completed_nonrecovery_censoring_and_crash_are_distinct(self):
        r = summarize([10, 10, 0, 0], [2], window=2)['recoveries'][0]
        self.assertEqual(r['status'], 'not_recovered')
        self.assertTrue(r['time_is_right_censored'])
        for reason in ('censored', 'crash'):
            result = summarize([10, 10, 0, 0], [2], window=2, planned_steps=8, end_reason=reason)
            r = result['recoveries'][0]
            self.assertEqual(r['status'], reason)
            self.assertEqual(r['time_is_right_censored'], reason == 'censored')
            self.assertIsNone(result['lifetime']['mean_reward'])
            self.assertEqual(result['lifetime']['observed_mean_reward'], 5)

    def test_next_change_ends_recovery_risk_window(self):
        result = summarize([10, 10, 0, 0, 10, 10], [2, 4], window=2)
        self.assertEqual(result['recoveries'][0]['status'], 'not_recovered')
        self.assertEqual(result['recoveries'][0]['terminal_event'], 'next_change')
        self.assertEqual(result['recoveries'][1]['baseline_mean'], 0)

    def test_scale_change_disables_recovery_claim(self):
        result = summarize([1, 1, 10, 10], [2], window=2, same_reward_scale=False)
        self.assertEqual(result['recoveries'][0]['status'], 'not_comparable')
        self.assertIsNone(result['recoveries'][0]['threshold'])

    def test_baseline_cannot_cross_an_earlier_change(self):
        result = summarize([1, 1, 1, 8, 9, 9, 9], [3, 4], window=2, baseline_window=3)
        self.assertEqual(result['recoveries'][1]['status'], 'insufficient_baseline')

    def test_unobserved_and_insufficient_baseline(self):
        result = summarize([1, 1], [1, 3], window=2, planned_steps=5, end_reason='crash')
        self.assertEqual([r['status'] for r in result['recoveries']], ['insufficient_baseline', 'not_observed'])
        self.assertEqual([s['observed_steps'] for s in result['segments']], [1, 1, 0])

    def test_recovery_before_later_crash_is_retained(self):
        result = summarize([1, 1, 2, 2, 0], [2], window=2, planned_steps=8, end_reason='crash')
        self.assertEqual(result['recoveries'][0]['status'], 'recovered')
        self.assertEqual(result['lifetime']['end_reason'], 'crash')
        self.assertFalse(result['lifetime']['complete'])

    def test_invalid_inputs_fail_without_fabricated_statistics(self):
        cases = [dict(rewards=[1, float('nan')], changes=[]),
                 dict(rewards=[1, 2], changes=[1, 1]),
                 dict(rewards=[1, 2], changes=[True]),
                 dict(rewards=[1, 2], changes=[], planned_steps=4),
                 dict(rewards=[1, 2], changes=[], tolerance=-1)]
        for kwargs in cases:
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                summarize(window=2, **kwargs)

    def test_empty_crash_has_no_mean(self):
        result = summarize([], [2], window=2, planned_steps=4, end_reason='crash')
        self.assertIsNone(result['lifetime']['observed_mean_reward'])
        self.assertEqual(result['recoveries'][0]['status'], 'not_observed')


if __name__ == '__main__':
    unittest.main()
