"""
Care Transition Efficiency & Placement Outcome Analytics
Dynamic Pipeline Simulation Module
"""

import pandas as pd
import numpy as np
from typing import Dict, Any

def run_pipeline_simulation(
    days: int = 90,
    initial_cbp: int = 50,
    initial_hhs: int = 2500,
    daily_intake_mean: float = 50.0,
    daily_intake_std: float = 15.0,
    transfer_efficiency_rate: float = 0.70, # Transfers = cbp * rate
    transfer_capacity_cap: float = 500.0,
    discharge_effectiveness_rate: float = 0.025, # Discharges = hhs * rate
    discharge_capacity_cap: float = 300.0,
    random_seed: int = 42
) -> pd.DataFrame:
    """
    Simulate care transition flow dynamics forward in time using discrete difference equations.
    
    CBP_t = CBP_{t-1} + Intake_t - Transfers_t
    HHS_t = HHS_{t-1} + Transfers_t - Discharges_t
    
    Transfers_t = min(CBP_{t-1} * transfer_efficiency_rate, transfer_capacity_cap)
    Discharges_t = min(HHS_{t-1} * discharge_effectiveness_rate, discharge_capacity_cap)
    """
    if random_seed is not None:
        np.random.seed(random_seed)
        
    records = []
    cbp = float(initial_cbp)
    hhs = float(initial_hhs)
    cumulative_backlog = 0.0
    
    for t in range(1, days + 1):
        # Stochastic intake (truncated at 0)
        intake = max(0.0, float(np.random.normal(daily_intake_mean, daily_intake_std)))
        
        # CBP transfers
        desired_transfers = cbp * transfer_efficiency_rate
        transfers = min(desired_transfers, transfer_capacity_cap, cbp + intake)
        
        # Update CBP
        cbp_next = max(0.0, cbp + intake - transfers)
        
        # HHS discharges
        desired_discharges = hhs * discharge_effectiveness_rate
        discharges = min(desired_discharges, discharge_capacity_cap, hhs + transfers)
        
        # Update HHS
        hhs_next = max(0.0, hhs + transfers - discharges)
        
        # Estimated Dwell Time (Little's Law)
        est_days_cbp = (cbp_next / transfers) if transfers > 0 else (cbp_next / 1e-3)
        est_days_hhs = (hhs_next / discharges) if discharges > 0 else (hhs_next / 1e-3)
        
        flores_breach = est_days_cbp > 3.0
        net_imbalance = intake - discharges
        cumulative_backlog += net_imbalance
        
        records.append({
            "Day": t,
            "Intake": round(intake, 1),
            "CBP_Custody": round(cbp_next, 1),
            "Transfers": round(transfers, 1),
            "HHS_Care": round(hhs_next, 1),
            "Discharges": round(discharges, 1),
            "Est_Days_CBP": round(est_days_cbp, 2),
            "Est_Days_HHS": round(est_days_hhs, 2),
            "Flores_Breach": flores_breach,
            "Net_Imbalance": round(net_imbalance, 1),
            "Cumulative_Backlog": round(cumulative_backlog, 1)
        })
        
        cbp = cbp_next
        hhs = hhs_next
        
    sim_df = pd.DataFrame(records)
    return sim_df


def evaluate_scenario_summary(sim_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Summarize key outcomes of a simulation run.
    """
    total_intake = sim_df['Intake'].sum()
    total_transfers = sim_df['Transfers'].sum()
    total_discharges = sim_df['Discharges'].sum()
    breach_days = sim_df['Flores_Breach'].sum()
    breach_pct = (breach_days / len(sim_df)) * 100
    
    return {
        "simulation_horizon_days": len(sim_df),
        "total_simulated_intake": round(total_intake, 0),
        "total_simulated_transfers": round(total_transfers, 0),
        "total_simulated_discharges": round(total_discharges, 0),
        "end_cbp_custody": round(sim_df['CBP_Custody'].iloc[-1], 0),
        "end_hhs_care": round(sim_df['HHS_Care'].iloc[-1], 0),
        "avg_cbp_dwell_days": round(sim_df['Est_Days_CBP'].mean(), 2),
        "avg_hhs_dwell_days": round(sim_df['Est_Days_HHS'].mean(), 1),
        "flores_breach_days": int(breach_days),
        "flores_breach_rate_pct": round(breach_pct, 1),
        "cumulative_net_backlog": round(sim_df['Cumulative_Backlog'].iloc[-1], 0)
    }


if __name__ == "__main__":
    df_sim = run_pipeline_simulation(days=60)
    summary = evaluate_scenario_summary(df_sim)
    print("Simulation summary (Baseline 60 Days):")
    for k, v in summary.items():
        print(f"  {k}: {v}")
