"""
Unit tests for Care Transition Efficiency & Placement Outcome Analytics
Compatible with Python standard library unittest and pytest
"""

import unittest
import pandas as pd
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from data_processor import load_and_clean_data, compute_pipeline_metrics, get_full_processed_dataset
from metrics import compute_summary_kpis, compute_spc_control_limits, compute_temporal_patterns, compute_regime_comparison
from simulation import run_pipeline_simulation, evaluate_scenario_summary

class TestCareTransitionAnalytics(unittest.TestCase):

    def test_load_and_clean_data(self):
        df = load_and_clean_data()
        self.assertFalse(df.empty)
        self.assertEqual(len(df), 720)
        self.assertIn('Date', df.columns)
        self.assertIn('Apprehensions', df.columns)
        self.assertIn('CBP_Custody', df.columns)
        self.assertIn('Transfers', df.columns)
        self.assertIn('HHS_Care', df.columns)
        self.assertIn('Discharges', df.columns)
        self.assertEqual(df['Date'].isna().sum(), 0)
        self.assertTrue(df['Date'].is_monotonic_increasing)

    def test_compute_pipeline_metrics(self):
        df = load_and_clean_data()
        processed = compute_pipeline_metrics(df)
        
        expected_cols = [
            'Transfer_Efficiency', 'Discharge_Effectiveness', 'Pipeline_Throughput',
            'Est_Days_CBP', 'Est_Days_HHS', 'Flores_Breach',
            'CBP_Net_Flow', 'HHS_Net_Flow', 'System_Net_Flow',
            'Cumulative_System_Net', 'Outcome_Stability_Score'
        ]
        for col in expected_cols:
            self.assertIn(col, processed.columns)
            
        valid_mask = (processed['Transfers'] > 0) & (processed['CBP_Custody'] > 0)
        np.testing.assert_allclose(
            processed.loc[valid_mask, 'Est_Days_CBP'],
            processed.loc[valid_mask, 'CBP_Custody'] / processed.loc[valid_mask, 'Transfers']
        )
        
        breach_sample = processed[processed['Est_Days_CBP'] > 3.0]
        self.assertTrue((breach_sample['Flores_Breach'] == True).all())

    def test_compute_summary_kpis(self):
        data = get_full_processed_dataset()
        kpis = compute_summary_kpis(data)
        
        self.assertEqual(kpis['total_days_reported'], 720)
        self.assertGreater(kpis['total_apprehensions'], 0)
        self.assertGreater(kpis['total_transfers'], 0)
        self.assertGreater(kpis['total_discharges'], 0)
        self.assertTrue(0 <= kpis['flores_compliance_pct'] <= 100)
        self.assertGreater(kpis['avg_transfer_efficiency'], 0)
        self.assertGreater(kpis['avg_discharge_effectiveness'], 0)

    def test_spc_control_limits(self):
        data = get_full_processed_dataset()
        spc = compute_spc_control_limits(data, 'Transfer_Efficiency')
        
        self.assertGreater(spc['center_line'], 0)
        self.assertGreater(spc['ucl'], spc['center_line'])
        self.assertLessEqual(spc['lcl'], spc['center_line'])
        self.assertGreater(spc['std_dev'], 0)
        self.assertGreaterEqual(spc['out_of_control_count'], 0)

    def test_regime_comparison(self):
        data = get_full_processed_dataset()
        regime_df = compute_regime_comparison(data)
        
        self.assertFalse(regime_df.empty)
        self.assertIn('Metric', regime_df.columns)
        self.assertIn('2023-2024 (Surge Mean)', regime_df.columns)
        self.assertIn('2025 (Stagnation Mean)', regime_df.columns)
        self.assertIn('p-value', regime_df.columns)

    def test_simulation_engine(self):
        sim = run_pipeline_simulation(days=30, initial_cbp=40, initial_hhs=2000, random_seed=42)
        self.assertEqual(len(sim), 30)
        self.assertIn('Intake', sim.columns)
        self.assertIn('CBP_Custody', sim.columns)
        self.assertIn('Transfers', sim.columns)
        self.assertIn('HHS_Care', sim.columns)
        self.assertIn('Discharges', sim.columns)
        self.assertIn('Est_Days_CBP', sim.columns)
        self.assertIn('Cumulative_Backlog', sim.columns)
        
        summary = evaluate_scenario_summary(sim)
        self.assertEqual(summary['simulation_horizon_days'], 30)
        self.assertGreater(summary['total_simulated_intake'], 0)
        self.assertTrue(0 <= summary['flores_breach_rate_pct'] <= 100)

if __name__ == '__main__':
    unittest.main()
