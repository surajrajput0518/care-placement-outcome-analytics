# Project Feedback Video: Presentation Script & Recording Guide

This document provides a comprehensive script and step-by-step recording guide for your **Project Feedback Video submission** (3 to 5 minutes duration). You can record this using **Loom**, **Zoom**, or screen recorder and upload to YouTube (as Unlisted) or Google Drive (set to "Anyone with the link can view").

---

## 📋 Video Overview & Metadata
- **Recommended Length:** 3 – 5 minutes
- **Recording Tools:** Loom (recommended for fast recording), Zoom Screen Recording, OBS, or Google Drive screen capture.
- **Visuals on Screen:** Open your browser with the live **Streamlit Dashboard** (`http://localhost:8501`) and the GitHub repository or code editor.
- **Key Submission Requirement:** Valid URL starting with `https://` (e.g., Loom link, unlisted YouTube link, or public Google Drive link).

---

## 🎬 Section-by-Section Speaking Script

### 0:00 – 0:45 | Section 1: Project Introduction & Problem Statement
*(Screen showing Streamlit App - Overview Tab with KPI cards and Sankey diagram)*

> "Hello everyone, my name is **[Your Name]**, and today I am excited to present my project on **Care Transition Efficiency & Placement Outcome Analytics** for the Unaccompanied Children Program.
>
> The UAC program operates as a critical multi-agency humanitarian care pipeline: children are apprehended by Border Patrol (CBP), transferred to the Department of Health and Human Services (HHS), sheltered, and ultimately reunified with vetted sponsors.
>
> While government dashboards historically monitor aggregate custody counts, process efficiency and transition velocity have remained hidden. My goal was to answer critical questions: How fast do children move between stages? Are discharges keeping pace with border inflows? Where do backlogs accumulate, and are placement outcomes improving over time?"

---

### 0:45 – 1:45 | Section 2: Analytical Methodology & Surprising Findings
*(Screen showing Tab 2: Transition & Placement Efficiency and Tab 3: Bottleneck Analytics)*

> "To analyze the 720 reporting dates from 2023 through 2025, I formulated the system as a tandem queueing network and applied **Little's Law** ($W = L / \lambda$) to estimate stage dwell times. I also developed key process KPIs:
> - **Transfer Efficiency Ratio:** velocity of clearing CBP custody
> - **Discharge Effectiveness Index:** daily rate of sponsor placements
> - **Pipeline Throughput:** system equilibrium ratio
>
> When analyzing the data, I discovered a major empirical paradox:
> In 2023 and 2024, when border arrivals were high (averaging 133 children per day), CBP dwell time averaged just 1.3 days—well within the statutory 72-hour Flores Settlement Agreement limit.
> 
> However, in 2025, when daily arrivals collapsed by over 90% down to just 13 children per day, **CBP dwell time jumped to 3.32 days**, exceeding the Flores statutory limit! In fact, **38.5% of reporting days in 2025 suffered Flores violations**, reaching over 73% by December 2025. 
> Why? Because lower intake caused field sectors to hold children to batch transport manifests. Furthermore, length of stay in HHS care surged from 34 days to over 226 days—more than 7 months—revealing severe stagnation for residual cases."

---

### 1:45 – 3:00 | Section 3: Live Application Walkthrough
*(Interactively clicking through the Streamlit tabs)*

> "To make these insights actionable for policymakers and agency leaders, I engineered an interactive Streamlit application with six core modules:
> 
> 1. **Pipeline Flow Architecture:** Here we have an interactive Sankey diagram tracing total flows from Apprehension through CBP, HHS, and sponsor discharge.
> 2. **Efficiency & Dwell Time Panels:** Here we track Little's Law dwell times with statutory threshold alert lines.
> 3. **Bottleneck & Backlog Tracker:** This visualizes cumulative stock-flow deficits and performs automated Welch's t-tests between the Surge and Stagnation regimes.
> 4. **Temporal Patterns & Statistical Process Control:** Here we implemented Shewhart $\bar{X}$ control charts to distinguish normal variations from systemic disruptions, along with day-of-week batching analysis.
> 5. **Policy Scenario Simulator:** Here decision-makers can stress-test interventions—such as increasing CBP transit velocity or HHS case worker capacity—to see projected backlogs and Flores compliance over 30, 60, or 90 days.
> 6. **Data Explorer:** Allows full inspection and filtered CSV export of the preprocessed dataset."

---

### 3:00 – 3:45 | Section 4: Experience, Learnings & Technical Growth
*(Screen showing Codebase / GitHub repo)*

> "Reflecting on my experience building this project:
> 1. **Data Engineering & Quality:** Working with real federal reporting data taught me the importance of handling data anomalies, missing dates, and calendar reporting schedules (like the Sunday–Thursday publishing cycle).
> 2. **Queueing Theory in Real Policy:** Translating Little's Law and flow conservation into concrete policy metrics was immensely rewarding. It proved that data science can directly impact child welfare and legal compliance.
> 3. **Interactive Visual Storytelling:** Building executive-grade dashboards with Plotly and Streamlit allowed me to bridge deep statistical modeling with intuitive visual alerts."

---

### 3:45 – 4:15 | Section 5: Conclusion & Recommendations
*(Screen showing Executive Summary / Research Paper)*

> "To resolve these challenges, our policy report recommends:
> 1. Prohibiting manifest batching and deploying agile regional shuttles.
> 2. Real-time Flores countdown alerts at the 48-hour mark.
> 3. Dedicated rapid-placement task forces to resolve long-stay HHS caseloads.
>
> Thank you so much for watching my project presentation!"

---

## 📹 How to Record and Host Your Video Link

1. **Option A (Fastest - Loom):**
   - Go to [Loom.com](https://www.loom.com) (free account).
   - Click "Record a Video" -> Select "Screen + Camera" or "Screen Only".
   - Open `http://localhost:8501` in your browser.
   - Follow the script above.
   - Loom gives you an instant `https://www.loom.com/share/...` link to paste into the submission form.

2. **Option B (YouTube Unlisted):**
   - Record using Zoom (Start meeting with screen share -> Record to computer) or Windows Game Bar (`Win + Alt + R`).
   - Upload to YouTube -> Set visibility to **"Unlisted"** (anyone with the link can view, but not public).
   - Copy the `https://youtu.be/...` link.

3. **Option C (Google Drive):**
   - Save your MP4 recording to Google Drive.
   - Right click -> Share -> Change to **"Anyone with the link can view"**.
   - Copy the `https://drive.google.com/file/d/...` link.
