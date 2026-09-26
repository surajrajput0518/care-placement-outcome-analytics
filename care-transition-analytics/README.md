# Care Transition Efficiency & Placement Outcome Analytics

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-FF4B4B.svg)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-5.0%2B-3F4F75.svg)](https://plotly.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An end-to-end data science, queueing theory, and process analytics platform evaluating the **U.S. Unaccompanied Children (UAC) Care Pipeline** across 720 reporting dates (January 2023 – December 2025).

---

## 📌 Executive Overview

The UAC Program operates a multi-agency humanitarian care and placement pipeline:
1. **Border Patrol (CBP) Custody:** Initial intake and physical custody.
2. **Interagency Transfer:** Statutory requirement to transfer custody to HHS within **72 hours** (*Flores Settlement Agreement* / TVPRA).
3. **HHS / Office of Refugee Resettlement (ORR) Care:** Sheltering, medical/psychological evaluations, and case management.
4. **Sponsor Discharge:** Successful placement with vetted family sponsors or legal guardians.

While conventional oversight focuses on static bed counts, this platform models **transition velocity, Little's Law dwell times, bottleneck accumulation, and Statistical Process Control (SPC)**.

---

## 🔍 Key Findings & Policy Paradox

| Dimension | Surge Regime (2023–2024) | Stagnation Regime (2025) | Impact | Statistical Significance |
| :--- | :---: | :---: | :---: | :---: |
| **Daily Apprehensions** | 133.5 / day | 13.0 / day | **-90.2%** | $p < 0.0001$ |
| **Transfers to HHS** | 184.4 / day | 16.6 / day | **-91.0%** | $p < 0.0001$ |
| **CBP Dwell Time (Flores Limit: 72h)** | **32.2 hours (1.34d)** | **79.7 hours (3.32d)** | **+147.6% (Breach)** | $p < 0.0001$ |
| **Flores 72-Hour Breach Rate** | **0.8% of days** | **38.5% of days (Peak: 73.3%)** | **Critical Non-Compliance** | $p < 0.0001$ |
| **HHS Length of Stay (LOS)** | **34.2 days (~5 wks)** | **226.9 days (~7.5 mos)** | **+564.1% (Stagnation)** | $p < 0.0001$ |

**The Low-Inflow Operational Paradox:** Even though border encounters dropped by 90%, CBP transition velocity degraded because field sectors began **batching smaller cohorts to fill transport manifests**, violating the 72-hour statutory Flores threshold.

---

## 🏗️ System Architecture

```mermaid
flowchart LR
    A["Border Apprehensions<br/>(CBP Intake)"] --> B["CBP Custody Buffer<br/>(Holding Stations)"]
    B -->|"Transfer Velocity<br/>(Target: <72 hrs)"| C["Interagency Transfers"]
    C --> D["HHS Shelter Buffer<br/>(ORR Facilities)"]
    D -->|"Discharge Velocity<br/>(Target: ~35 days)"| E["Sponsor Placements<br/>(Reunification)"]

    style A fill:#3b82f6,stroke:#1d4ed8,color:#fff
    style B fill:#f59e0b,stroke:#b45309,color:#fff
    style C fill:#8b5cf6,stroke:#6d28d9,color:#fff
    style D fill:#ec4899,stroke:#be185d,color:#fff
    style E fill:#10b981,stroke:#047857,color:#fff
```

---

## 💻 Tech Stack & Features

- **Frontend & UI:** Streamlit with custom CSS, executive metric cards, and responsive tabs.
- **Interactive Visualizations:** Plotly Express & Plotly Graph Objects (Interactive Sankey Flow, Dwell Time Curves, Shewhart SPC Charts, Cumulative Backlog Fill).
- **Analytics Engine:** NumPy, SciPy (Welch's $t$-tests), Pandas, Little's Law formulations.
- **Dynamic Simulation:** Difference equation discrete-event simulator for capacity planning.
- **Testing:** Python standard `unittest` and `pytest` compatible suite.

---

## 🚀 Quick Start & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/care-transition-analytics.git
cd care-transition-analytics
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit Dashboard
```bash
streamlit run app.py
# or
python -m streamlit run app.py
```
Open your browser at `http://localhost:8501`.

### 4. Run Automated Unit Tests
```bash
python -m unittest discover -s tests -p "test_*.py"
```

---

## 📂 Project Structure

```
care-transition-analytics/
├── data/
│   ├── raw_uac_data.csv               # Raw UAC daily operational data (2023-2025)
│   └── processed_uac_pipeline.csv     # Enriched feature matrix with queue metrics
├── src/
│   ├── __init__.py
│   ├── data_processor.py              # ETL, Little's Law dwell times, Flores flags
│   ├── metrics.py                     # KPIs, Shewhart SPC control limits, Welch's t-tests
│   └── simulation.py                  # Dynamic policy & capacity stress-testing sandbox
├── reports/
│   ├── research_paper.md              # Full academic research paper with citations
│   ├── executive_summary.md           # Policy briefing for DHS, HHS, & Congress
│   └── project_feedback_video_script.md # Script & guide for submission video
├── tests/
│   ├── __init__.py
│   └── test_analytics.py              # Comprehensive automated unit test suite
├── app.py                             # Main Streamlit web application
├── requirements.txt                   # Dependency manifest
└── README.md                          # Project documentation
```

---

## 🌐 Deploying to Streamlit Community Cloud (Free & 1-Click)

1. Push this repository to your GitHub account:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Care Transition Analytics Platform"
   git branch -M main
   git remote add origin https://github.com/<your-username>/care-transition-analytics.git
   git push -u origin main
   ```
2. Navigate to [share.streamlit.io](https://share.streamlit.io/).
3. Click **"New app"** -> Select your repository, branch (`main`), and main file path (`app.py`).
4. Click **Deploy!** Your app will be live at `https://<your-app-name>.streamlit.app`.

---

## 📜 Citation & License

This project is licensed under the MIT License.
If utilizing this methodology or empirical findings, please cite:
> Unified Mentor Research Team. (2026). *Care Transition Efficiency & Placement Outcome Analytics: A Multi-Stage Queueing and Empirical Evaluation of the U.S. Unaccompanied Children Care Pipeline (2023–2025)*.
