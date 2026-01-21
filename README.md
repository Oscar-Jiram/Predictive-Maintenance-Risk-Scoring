# Predictive Maintenance – Risk Scoring & Failure Analysis

## Project Overview
This project simulates a real-world **predictive maintenance analytics scenario** focused on identifying operational risk patterns and failure behavior in industrial machinery.  
The objective is to transform raw sensor and operational data into a **business-ready risk scoring framework** that supports proactive maintenance decisions, failure prevention, and operational efficiency.

The analysis combines **Python-based feature engineering and risk modeling** with **Tableau dashboards** to communicate insights clearly to technical and non-technical stakeholders.

---

## Business Context
In industrial environments, unplanned machine failures lead to production downtime, increased maintenance costs, and operational inefficiencies.  
While machines generate large volumes of sensor data, maintenance decisions are often reactive rather than preventive.

This project reflects a manufacturing setting where:
- Equipment reliability is critical  
- Failures are costly  
- Early risk detection can significantly reduce downtime and maintenance expenses  

The challenge is not only detecting failures, but **prioritizing risk before failures occur**.

---

## Objective
The goal of this project is to:
- Analyze historical machine and sensor data  
- Engineer meaningful operational risk indicators  
- Build a **continuous risk score** and **risk level segmentation**  
- Identify which operating conditions and machine types are most failure-prone  
- Deliver insights through a **clear, decision-oriented Tableau dashboard**

---

## Dataset Overview
- Source: AI4I 2020 Predictive Maintenance Dataset  
- Observations: Industrial machine operations  
- Data includes:
  - Temperatures  
  - Torque  
  - Rotational speed  
  - Tool wear  
  - Machine failure flags  
  - Specific failure modes (TWF, HDF, PWF, OSF, RNF)  

Cleaned and business-ready datasets are exported to the `export/` directory.

---

## Methodology

### 1. Data Preparation
- Removal of duplicates  
- Validation of operational ranges  
- Feature normalization  

### 2. Feature Engineering
Custom proxies were engineered to represent operational stress:
- **Temperature Delta**: Process vs air temperature  
- **Power Proxy**: Torque × Rotational Speed  
- **Wear Rate Proxy**: Tool wear relative to speed  

### 3. Risk Scoring Model
A composite risk score was constructed using normalized features:
- Torque (40%)  
- Tool wear (40%)  
- Power proxy (20%)  

The score represents **relative operational risk**, not a binary prediction.

### 4. Risk Segmentation
Machines were segmented into:
- Low risk  
- Medium risk  
- High risk  

(using quantile-based thresholds)

### 5. Failure Analysis
- Failure rate by risk level  
- Failure rate by machine type  
- Pareto analysis of failure modes  

---

## Executive Dashboard Overview
*High-level operational KPIs and risk distribution across the fleet.*

![alt text](<Dashboard Pareto Failure Modes.png>)

<img width="1360" height="556" alt="image" src="https://github.com/user-attachments/assets/752f2fb3-a315-4fa3-8ab0-702f3598921b" />


_This view summarizes global failure rate, risk distribution, and key operational indicators for decision-makers._

---

## Risk Segmentation & Failure Rates
*Understanding how failure probability increases with operational risk.*

<img width="1207" height="556" alt="image" src="https://github.com/user-attachments/assets/f5827906-7ab4-4063-9d4f-3fe46fce1468" />


_This visualization demonstrates how higher risk scores correlate with significantly increased failure rates._

---

## Failure Modes & Root Causes
*Identifying dominant failure mechanisms.*

<img width="1288" height="554" alt="image" src="https://github.com/user-attachments/assets/e17c3e28-02d7-4b51-bb00-eba8e286c51c" />


_The Pareto chart highlights which failure types account for the majority of incidents, supporting targeted preventive actions._

---

## Machine Type Performance
*Comparing reliability across machine categories.*

<img width="1250" height="557" alt="image" src="https://github.com/user-attachments/assets/a65b21c9-c9e6-460d-90b5-a62f453dc2c3" />


_This view reveals differences in reliability across machine types, supporting differentiated maintenance strategies._

---

## Key Findings
- Failure rates increase significantly as operational risk scores rise.  
- A small number of failure modes account for the majority of incidents.  
- Certain machine types exhibit consistently higher failure rates.  
- Risk scoring provides earlier insight than binary failure flags alone.  
- Preventive maintenance strategies can be prioritized using risk segmentation.  

---

## Business Implications
- Reactive maintenance leads to avoidable downtime and costs.  
- Risk-based prioritization enables more efficient maintenance planning.  
- Early intervention on high-risk machines reduces failure impact.  
- Data-driven maintenance outperforms calendar-based schedules.  

---

## Recommendations
- Implement risk-based maintenance scheduling.  
- Monitor high-risk machines more frequently.  
- Focus preventive actions on dominant failure modes.  
- Integrate risk scores into operational dashboards and alerts.  

---

## Limitations
- The analysis is based on historical transactional data only.  
- External factors such as maintenance quality and operator behavior are not included.  
- Risk score represents relative risk, not exact failure probability.  

---

## Next Steps
- Incorporate time-series modeling.  
- Add remaining useful life (RUL) estimation.  
- Integrate real-time sensor streams.  
- Compare rule-based vs ML-based risk models.  

---

## Tools & Technologies
- Python (Pandas, NumPy, Matplotlib)  
- Tableau  
- Jupyter Notebook  
- Git & GitHub  

---

## Repository Structure

predictive-maintenance-risk-scoring/
│
├── export/ # Business-ready datasets
├── outputs/ # Generated plots
├── predictive_maintenance_risk_score.py
├── README.md
└── ai4i2020.csv
