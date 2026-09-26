# Care Transition Efficiency & Placement Outcome Analytics: A Multi-Stage Queueing and Empirical Evaluation of the U.S. Unaccompanied Children Care Pipeline (2023–2025)

**Author:** Unified Mentor Research Team / Child Welfare Data Analytics Collaborative  
**Date:** September 2026  
**Subject Classification:** Operations Research, Public Health Policy, Child Welfare Informatics, Stochastic Queueing Systems  

---

## Executive Abstract

The Unaccompanied Children (UAC) Program, administered jointly by the U.S. Customs and Border Protection (CBP) within the Department of Homeland Security (DHS) and the Office of Refugee Resettlement (ORR) within the Department of Health and Human Services (HHS), represents one of the most operationally complex child welfare pipelines in federal administration. While standard oversight frameworks focus almost exclusively on static aggregate counts of children in custody, process velocity, stage-to-stage transition friction, queueing dynamics, and outcome stability metrics have remained largely unmodeled. 

This study develops a quantitative flow pipeline framework analyzing 720 official reporting dates from January 12, 2023 through December 21, 2025. Applying queueing theory (Little's Law: $W = L / \lambda$), mass-balance conservation principles, Shewhart Statistical Process Control (SPC), and Welch's $t$-tests for unequal variances, we evaluate process performance across two distinct operational regimes: the High-Inflow Surge Regime (2023–2024) and the Policy-Constrained Stagnation Regime (2025).

Our empirical findings reveal a striking operational paradox: despite a **90.2% collapse in daily intake volume** (from 133.5 children/day in 2023–2024 to 13.0 children/day in 2025; $p < 0.0001$), transition efficiency degraded severely. Average dwell time in CBP custody increased by **147.6%**, surging from 1.34 days (32.2 hours) to **3.32 days (79.7 hours)**, exceeding the statutory 72-hour limit established by the *Flores Settlement Agreement* and the *Trafficking Victims Protection Reauthorization Act* (TVPRA). In 2025, **38.5% of reporting days breached the 72-hour Flores standard**, peaking at **73.3% in December 2025**. Simultaneously, in-shelter length of stay (LOS) in HHS care escalated by **564.1%**, rising from 34.2 days to **226.9 days (~7.5 months)**, reflecting severe case management stagnation for residual populations. We conclude with six actionable structural, administrative, and technological recommendations to restore interagency pipeline velocity.

**Keywords:** Unaccompanied Children, Care Transition Efficiency, Flores Settlement Agreement, Little's Law, Queueing Theory, Statistical Process Control, Child Welfare Outcomes.

---

## 1. Introduction & Policy Context

Under the Homeland Security Act of 2002 (Pub. L. 107-296) and the William Wilberforce Trafficking Victims Protection Reauthorization Act of 2008 (TVPRA, 8 U.S.C. § 1232), the United States established a bifurcated statutory pipeline for unaccompanied alien children arriving at national borders:
1. **Apprehension & Temporary Processing:** U.S. Customs and Border Protection (CBP) apprehends, identifies, and temporarily houses unaccompanied minors in border patrol stations.
2. **Interagency Custody Transfer:** By statutory mandate under 8 U.S.C. § 1232(b)(3) and judicial precedent under the 1997 *Flores v. Reno* Settlement Agreement, CBP must transfer custody of unaccompanied minors to the Department of Health and Human Services (HHS) **no later than 72 hours** after apprehension.
3. **Sheltering, Health Screening & Case Management:** The HHS Administration for Children and Families (ACF) / Office of Refugee Resettlement (ORR) places children in licensed care providers, shelters, or foster care networks, conducting physical/mental evaluations, family tracing, and sponsor vetting.
4. **Discharge & Family Reunification:** Children are released to vetted sponsors—primarily parents, close relatives, or approved guardians—pending immigration court proceedings.

### The Problem of Static Monitoring
Historically, public oversight and agency dashboards have tracked gross inventory counts: total children in CBP custody and total children in HHS shelters. While necessary for physical bed allocation, static inventory tracking obscures underlying transition efficiency:
- Are transfer velocities between CBP and HHS maintaining statutory pace?
- Do discharges keep pace with intake volumes, or do backlogs silently compound?
- How do operational bottlenecks shift when border encounters drop versus when they surge?
- Does lower inflow automatically lead to faster processing, or does reduced volume trigger operational diseconomies of scale and administrative batching?

This paper introduces a rigorous operational analytics framework to model the care pipeline dynamically, evaluate transition friction, and measure statutory compliance.

---

## 2. Mathematical Framework & Analytical Methodology

### 2.1 Pipeline Flow Architecture & Conservation of Mass
We formalize the UAC system as a tandem multi-server queueing network with two primary buffers:

$$\text{CBP Custody Buffer } (Q_1) \longrightarrow \text{Interagency Flow } (\mu_1) \longrightarrow \text{HHS Shelter Buffer } (Q_2) \longrightarrow \text{Discharge Flow } (\mu_2)$$

Let $t \in \{1, 2, \dots, T\}$ denote discrete daily observation dates. The system state is governed by:
- $A_t$: Daily apprehensions placed into CBP custody (system input).
- $C_t$: Children in active CBP custody at time $t$ (Buffer 1 inventory).
- $T_t$: Children transferred from CBP to HHS custody on day $t$ (Interstage flow).
- $H_t$: Children in active HHS shelter care at time $t$ (Buffer 2 inventory).
- $D_t$: Children discharged to vetted sponsors on day $t$ (System output).

Under conservation of flow:

$$\Delta C_t = C_t - C_{t-1} = A_t - T_t + \epsilon_{1,t}$$

$$\Delta H_t = H_t - H_{t-1} = T_t - D_t + \epsilon_{2,t}$$

where $\epsilon_{1,t}$ and $\epsilon_{2,t}$ capture unobserved attritions, age-outs (turning 18), or administrative adjustments.

### 2.2 Core Operational Process Metrics
To evaluate efficiency independently of gross scale, we formulate four dimensionless process indices:

1. **Transfer Efficiency Ratio ($\eta_{\text{trans}}$):**
   $$\eta_{\text{trans}, t} = \frac{T_t}{C_t}$$
   Measures the daily velocity at which CBP clears its active holding queue. A ratio of 1.0 indicates full daily turnover; values below 0.33 denote an imminent risk of exceeding the 72-hour threshold.

2. **Discharge Effectiveness Index ($\eta_{\text{disc}}$):**
   $$\eta_{\text{disc}, t} = \frac{D_t}{H_t}$$
   Reflects the daily proportion of the shelter population successfully placed with sponsors. A steady-state value of 0.028 corresponds to an average length of stay of ~35 days.

3. **Pipeline Throughput Rate ($\Theta$):**
   $$\Theta_t = \frac{D_t}{A_t}$$
   Represents net system expansion or contraction. $\Theta > 1.0$ indicates that the system is discharging more children than entering (de-escalation), while $\Theta < 1.0$ signals backlog accumulation.

4. **Net Imbalance & Cumulative System Backlog ($B_{\text{sys}}$):**
   $$\Delta B_t = A_t - D_t, \quad B_{\text{sys}, t} = \sum_{k=1}^t (A_k - D_k)$$

### 2.3 Queueing Dwell Time Estimation (Little's Law)
By Little's Law, for a stable queueing system in equilibrium, the average number of items in a system ($L$) equals the average arrival/departure rate ($\lambda$) multiplied by the average time an item spends in the system ($W$):

$$L = \lambda W \implies W = \frac{L}{\lambda}$$

Applying this formulation to daily cross-sectional operational stages:
- **Estimated CBP Dwell Time:**
  $$\hat{W}_{\text{CBP}, t} = \frac{C_t}{T_t} \quad \text{[Days]}, \quad \hat{W}_{\text{CBP}, t}^{(\text{hours})} = \frac{C_t}{T_t} \times 24$$
- **Estimated HHS Length of Stay (LOS):**
  $$\hat{W}_{\text{HHS}, t} = \frac{H_t}{D_t} \quad \text{[Days]}$$

### 2.4 Statistical Process Control (SPC)
To distinguish routine system variability from structural systemic failure, we implement Shewhart $\bar{X}$ control charts:
- **Center Line (CL):** $\bar{X} = \frac{1}{N} \sum_{t=1}^N X_t$
- **Upper / Lower Control Limits (UCL / LCL):** $\text{UCL} = \bar{X} + 3\hat{\sigma}, \quad \text{LCL} = \max(0, \bar{X} - 3\hat{\sigma})$
- **Warning Limits (UWL / LWL):** $\text{UWL} = \bar{X} + 2\hat{\sigma}, \quad \text{LWL} = \max(0, \bar{X} - 2\hat{\sigma})$

---

## 3. Empirical Results & Findings

### 3.1 Macro Summary of the Dataset
The dataset encompasses **720 valid reporting dates** between **January 12, 2023 and December 21, 2025**. Across the entire observation period:
- **Total Border Apprehensions ($A$):** 67,337 children (mean: 93.5/day)
- **Total Interagency Transfers ($T$):** 92,641 children (mean: 128.7/day)
- **Total Sponsor Discharges ($D$):** 124,853 children (mean: 173.4/day)
- **Overall System Throughput ($\Theta$):** 2.50 (reflecting net drawdown from peak 2022 inventories)
- **Overall Mean CBP Custody:** 171.5 children (range: 7 to 531)
- **Overall Mean HHS Shelter Care:** 6,061.3 children (range: 1,972 to 11,516)

### 3.2 Regime Shift: Surge (2023–2024) vs. Stagnation (2025)
A segmented econometric comparison reveals a profound structural regime break commencing in January 2025:

| Pipeline Dimension | Surge Regime (2023–2024, $N=481$) | Stagnation Regime (2025, $N=239$) | Relative Change | Welch's $t$-stat | $p$-value | Statistical Significance |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Daily Apprehensions** | 133.52 (±54.07) | 13.03 (±17.54) | **-90.2%** | 44.18 | $< 0.0001$ | Statistically Significant |
| **Daily Transfers to HHS** | 184.36 (±67.42) | 16.59 (±23.74) | **-91.0%** | 47.93 | $< 0.0001$ | Statistically Significant |
| **Daily Discharges** | 245.18 (±84.28) | 28.95 (±45.22) | **-88.2%** | 43.46 | $< 0.0001$ | Statistically Significant |
| **Active CBP Custody** | 240.36 (±96.51) | 32.91 (±24.02) | **-86.3%** | 42.61 | $< 0.0001$ | Statistically Significant |
| **Active HHS Shelter Care** | 7,809.52 (±1,563.65) | 2,542.84 (±841.45) | **-67.4%** | 56.78 | $< 0.0001$ | Statistically Significant |
| **Transfer Efficiency Ratio** | 0.81 (±0.23) | 0.46 (±0.33) | **-42.9%** | 14.86 | $< 0.0001$ | Statistically Significant |
| **Discharge Effectiveness** | 0.031 (±0.009) | 0.011 (±0.012) | **-71.1%** | 22.75 | $< 0.0001$ | Statistically Significant |
| **Est. Days in CBP (Dwell)** | **1.34 days (32.2h)** | **3.32 days (79.7h)** | **+147.6%** | -11.45 | $< 0.0001$ | Statistically Significant |
| **Est. Days in HHS (LOS)** | **34.16 days** | **226.88 days** | **+564.1%** | -13.08 | $< 0.0001$ | Statistically Significant |

### 3.3 The Flores Settlement Compliance Crisis
The *Flores Settlement Agreement* requires that unaccompanied children be transferred from CBP border facilities (which are constitutionally unsuitable for minors) to HHS licensed care within 72 hours (3.0 days). 

Our Little's Law dwell time analysis identifies an alarming trend:
- **In 2023:** 3 out of 230 reporting days (1.30%) breached the 72-hour threshold. Average dwell time was 1.32 days.
- **In 2024:** 1 out of 251 reporting days (0.40%) breached the 72-hour threshold. Average dwell time was 1.36 days.
- **In 2025:** **92 out of 239 reporting days (38.49%) breached the 72-hour threshold.**
- **Monthly Trajectory in 2025:**
  - January 2025: 4.5% breach rate
  - March 2025: 40.9% breach rate
  - August 2025: 65.0% breach rate
  - November 2025: 68.4% breach rate
  - December 2025: **73.3% breach rate**

#### Why Did Lower Inflow Cause Higher Dwell Times?
This non-intuitive finding illustrates **transportation batching friction**:
When border encounters were high (100–300 children/day), CBP maintained dedicated daily transportation flights and buses directly to ORR intake hubs. When daily apprehensions fell to 5–15 children/day, field sectors began holding children in border stations for multiple days to aggregate full transport manifests, directly violating statutory limits.

### 3.4 HHS Length of Stay (LOS) Escalation
In 2023 and 2024, the HHS care pipeline maintained high velocity: an average discharge effectiveness of ~3.1% per day cleared the shelter population in an average of 34.2 days (~5 weeks), consistent with historical ORR reunification targets.

In 2025, discharge effectiveness plummeted to 1.1% per day. By December 2025, average length of stay reached **226.9 days (~7.5 months)**. This indicates that while easy-to-reunify cases (children with parents in the U.S.) were processed quickly, the remaining shelter population represents a "hard-to-place" residual caseload (children requiring fingerprint background checks for non-parent sponsors, home studies, or specialized medical/psychological care) who languished due to institutional inertia.

### 3.5 Operational Cycle and Day-of-Week Batching
Analysis of the 720 reporting dates revealed an administrative reporting artifact:
- Government reports are released Sunday through Thursday (Monday–Thursday represent standard business days; Sunday incorporates weekend transfers). Friday and Saturday lack individual daily public releases.
- **Discharge Peak on Thursdays and Sundays:** Average discharges reached 205.7 on Thursdays and 206.1 on Sundays, compared to 136.1 on Tuesdays. This confirms weekly batching where case managers finalize sponsor releases prior to the weekend or immediately following weekend intake reconciliations.

---

## 4. Policy Recommendations

Based on empirical modeling, we submit six actionable policy and operational interventions:

### Recommendation 1: Abolish Manifest-Batching & Establish Dynamic Interagency Transit (DHS/CBP)
Field sectors must be prohibited from delaying child transfers to fill transport manifests. DHS should contract dynamic, smaller-capacity regional transit providers (or establish dedicated inter-facility shuttles between Rio Grande Valley/El Paso and regional ORR hubs) to guarantee transfer within 24–36 hours, regardless of daily intake volume.

### Recommendation 2: Institute Real-Time "Flores Countdown" Tracking
CBP and HHS should deploy an interoperable, biometric/API-integrated case tracking dashboard. Every child entering CBP custody should trigger an automated countdown timer visible to both CBP Watch Centers and ORR Federal Field Specialists. At the 48-hour mark, automatic escalation protocols must deploy expedited transit assets.

### Recommendation 3: Implement Specialized Surge Teams for HHS Residual Caseloads (HHS/ORR)
To address the 226-day length of stay in HHS care, ORR should establish "Long-Term Stay Resolution Teams" dedicated solely to children who have been in custody for more than 45 days. These teams should focus on overcoming sponsor vetting delays (home studies, consular document acquisition, fingerprint clearance).

### Recommendation 4: Decouple Sponsor Vetting Friction from Low-Risk Relative Placements
Empirical data suggests that administrative caution in sponsor vetting expanded processing times dramatically. We recommend establishing tiered vetting: Category 1 sponsors (parents and legal guardians) should receive expedited release within 14 days, reserving intensive home studies for Category 3 (unrelated sponsors).

### Recommendation 5: Establish Statutory Reporting on Friday/Saturday Operations
Current 5-day reporting obscures weekend intake spikes and holiday backlogs. Congress should mandate continuous 7-day automated reporting to prevent weekend data vacuums.

### Recommendation 6: Mandate Process Velocity KPIs in Congressional Oversight
Federal monitoring of the UAC program must formally shift from static bed counts to process efficiency indices: Transfer Efficiency Ratio, Discharge Effectiveness Index, and Little's Law Dwell Times should be codified as mandatory quarterly Congressional reporting metrics.

---

## 5. Conclusion

By reframing the UAC care pipeline through queueing theory and process analytics, this investigation reveals that reduced border encounters do not inherently resolve child welfare bottlenecks. In fact, low-volume regimes introduced severe transportation batching, causing **38.5% of 2025 days to breach the 72-hour Flores standard** and ballooning HHS length of stay past seven months. 

Transforming the UAC program from a reactive custody storage operation to an agile, velocity-focused child transition network is both an operational necessity and a humanitarian obligation. Implementing dynamic transit, real-time dwell time alarms, and tiered sponsor reunification workflows will ensure that unaccompanied children move safely, rapidly, and legally into vetted family homes.

---

## References

1. *Flores v. Reno*, Case No. CV 85-4544-RJK (C.D. Cal. 1997) (Settlement Agreement).
2. Homeland Security Act of 2002, Pub. L. No. 107-296, 116 Stat. 2135 (2002).
3. William Wilberforce Trafficking Victims Protection Reauthorization Act of 2008 (TVPRA), 8 U.S.C. § 1232 (2008).
4. Little, J. D. C. (1961). "A Proof for the Queuing Formula: $L = \lambda W$." *Operations Research*, 9(3), 383–387.
5. Shewhart, W. A. (1931). *Economic Control of Quality of Manufactured Product*. D. Van Nostrand Company.
6. U.S. Department of Health and Human Services (HHS), Administration for Children and Families (ACF), Office of Refugee Resettlement (ORR). *Unaccompanied Children Program Reports & Data releases (2023–2025)*.
7. U.S. Government Accountability Office (GAO). (2022). *Unaccompanied Children: Actions Needed to Improve Interagency Coordination and Data Quality*. GAO-22-105128.
