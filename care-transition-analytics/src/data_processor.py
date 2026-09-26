"""
Care Transition Efficiency & Placement Outcome Analytics
Data Processor Module
"""

import pandas as pd
import numpy as np
import os

DEFAULT_RAW_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "raw_uac_data.csv"
)

COLUMN_MAPPING = {
    "Children apprehended and placed in CBP custody": "Apprehensions",
    "Children apprehended and placed in CBP custody*": "Apprehensions",
    "Children in CBP custody": "CBP_Custody",
    "Children transferred out of CBP custody": "Transfers",
    "Children in HHS Care": "HHS_Care",
    "Children discharged from HHS Care": "Discharges"
}

def load_and_clean_data(file_path: str = DEFAULT_RAW_PATH) -> pd.DataFrame:
    """
    Load raw UAC pipeline CSV data, sanitize column names, handle numeric conversions,
    and parse dates chronologically.
    """
    if not os.path.exists(file_path):
        # Fallback to local dataset.csv if raw_uac_data.csv not yet moved
        alt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dataset.csv")
        if os.path.exists(alt_path):
            file_path = alt_path
        else:
            raise FileNotFoundError(f"Dataset file not found at {file_path}")

    df = pd.read_csv(file_path)
    
    # Drop rows where Date is null (e.g. trailing empty rows in original CSV)
    df = df.dropna(subset=['Date']).copy()
    
    # Clean whitespace and asterisk in column names
    clean_cols = {}
    for col in df.columns:
        clean_name = col.strip().replace('*', '')
        clean_cols[col] = clean_name
    df = df.rename(columns=clean_cols)
    
    # Map to standardized pipeline variable names
    rename_dict = {
        "Children apprehended and placed in CBP custody": "Apprehensions",
        "Children in CBP custody": "CBP_Custody",
        "Children transferred out of CBP custody": "Transfers",
        "Children in HHS Care": "HHS_Care",
        "Children discharged from HHS Care": "Discharges"
    }
    df = df.rename(columns=rename_dict)
    
    # Sanitize numeric fields (remove commas, strip strings)
    num_cols = ["Apprehensions", "CBP_Custody", "Transfers", "HHS_Care", "Discharges"]
    for col in num_cols:
        if col in df.columns:
            if df[col].dtype == object:
                df[col] = df[col].astype(str).str.replace(',', '').str.strip()
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Parse dates
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date']).sort_values('Date').reset_index(drop=True)
    
    return df


def compute_pipeline_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Derive core flow ratios, Little's Law dwell times, Flores Settlement compliance flags,
    and cumulative stock-flow imbalance metrics.
    """
    df = df.copy()
    
    # Flow Ratios & Operational Efficiencies
    # Transfer Efficiency Ratio: Transfers / CBP Custody (velocity of clearing CBP custody)
    df['Transfer_Efficiency'] = df['Transfers'] / df['CBP_Custody'].replace(0, np.nan)
    
    # Discharge Effectiveness Index: Discharges / HHS Care (velocity of sponsor placements from shelter care)
    df['Discharge_Effectiveness'] = df['Discharges'] / df['HHS_Care'].replace(0, np.nan)
    
    # Overall Pipeline Throughput: Discharges / Apprehensions (system equilibrium ratio)
    df['Pipeline_Throughput'] = df['Discharges'] / df['Apprehensions'].replace(0, np.nan)
    
    # Little's Law Average Dwell Time Approximation: W = L / lambda
    # W_CBP: Average days in CBP custody = CBP_Custody / Transfers
    df['Est_Days_CBP'] = df['CBP_Custody'] / df['Transfers'].replace(0, np.nan)
    df['Est_Hours_CBP'] = df['Est_Days_CBP'] * 24.0
    
    # W_HHS: Average days in HHS care = HHS_Care / Discharges
    df['Est_Days_HHS'] = df['HHS_Care'] / df['Discharges'].replace(0, np.nan)
    
    # Statutory Flores Settlement Compliance Threshold (72 hours / 3.0 days in CBP custody)
    df['Flores_Breach'] = df['Est_Days_CBP'] > 3.0
    
    # Daily Net Accumulation / Backlog Rates
    df['CBP_Net_Flow'] = df['Apprehensions'] - df['Transfers']
    df['HHS_Net_Flow'] = df['Transfers'] - df['Discharges']
    df['System_Net_Flow'] = df['Apprehensions'] - df['Discharges']
    
    # Cumulative Backlog Trajectories
    df['Cumulative_CBP_Net'] = df['CBP_Net_Flow'].cumsum()
    df['Cumulative_HHS_Net'] = df['HHS_Net_Flow'].cumsum()
    df['Cumulative_System_Net'] = df['System_Net_Flow'].cumsum()
    
    # Temporal indicators
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['YearMonth'] = df['Date'].dt.to_period('M').astype(str)
    df['DayOfWeek'] = df['Date'].dt.day_name()
    df['DayOfWeekNum'] = df['Date'].dt.weekday
    df['IsWeekend'] = df['DayOfWeekNum'] >= 5
    
    # Operational Regime Flag
    # 2023-2024 was High-Inflow / Active Surges; 2025 was Policy-Constrained Inflow / Stagnation
    df['Operational_Regime'] = np.where(df['Year'] < 2025, 'High Inflow (2023-2024)', 'Stagnation Regime (2025)')
    
    # Rolling Moving Averages (7-day and 30-day)
    rolling_cols = [
        'Apprehensions', 'CBP_Custody', 'Transfers', 'HHS_Care', 'Discharges',
        'Transfer_Efficiency', 'Discharge_Effectiveness', 'Pipeline_Throughput',
        'Est_Days_CBP', 'Est_Days_HHS', 'System_Net_Flow'
    ]
    
    for col in rolling_cols:
        df[f'{col}_7d_MA'] = df[col].rolling(window=7, min_periods=1).mean()
        df[f'{col}_30d_MA'] = df[col].rolling(window=30, min_periods=1).mean()
        df[f'{col}_7d_STD'] = df[col].rolling(window=7, min_periods=2).std().fillna(0)
    
    # Outcome Stability Score: Inverse of rolling coefficient of variation for discharges
    # High score = steady, predictable placement rate; Low score = erratic, unstable placement velocity
    rolling_cv_discharges = (df['Discharges_7d_STD'] / df['Discharges_7d_MA'].replace(0, np.nan)).fillna(0)
    df['Outcome_Stability_Score'] = (1.0 / (1.0 + rolling_cv_discharges)).clip(0, 1)
    
    return df


def get_full_processed_dataset(file_path: str = DEFAULT_RAW_PATH) -> pd.DataFrame:
    """
    Single invocation pipeline that returns the fully preprocessed and enriched dataset.
    """
    raw_df = load_and_clean_data(file_path)
    processed_df = compute_pipeline_metrics(raw_df)
    return processed_df


if __name__ == "__main__":
    df = get_full_processed_dataset()
    print(f"Data processing complete. Processed {len(df)} records.")
    print("Columns:", df.columns.tolist()[:15], "...")
    out_csv = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "processed_uac_pipeline.csv")
    df.to_csv(out_csv, index=False)
    print(f"Saved processed dataset to {out_csv}")
