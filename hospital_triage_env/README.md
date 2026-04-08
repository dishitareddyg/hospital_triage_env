# 🏥 AI-Powered Hospital Triage System

## 🚨 Problem Statement
Emergency departments often suffer from **overcrowding, inefficient patient prioritization, and limited medical resources**.  
This leads to:
- Increased patient waiting times  
- Poor resource utilization  
- Higher risk for critical patients  

---

## 💡 Solution Overview
We developed a **simulation-based Hospital Triage System** that uses intelligent decision-making to:

- Dynamically manage incoming patients  
- Prioritize patients based on severity  
- Allocate doctors efficiently  
- Compare baseline vs AI-driven strategies  

The system demonstrates how **AI can improve hospital workflow under real-world constraints**.

---

## ⚙️ Tech Stack

- **Language:** Python  
- **Simulation Engine:** Custom Environment  
- **AI Approach:** Heuristic-based (extendable to Reinforcement Learning)  
- **Architecture:** Modular (Environment + Simulator + Evaluation)

---

## 🧠 System Architecture
# 🏥 AI-Powered Hospital Triage System

## 🚨 Problem Statement
Emergency departments often suffer from **overcrowding, inefficient patient prioritization, and limited medical resources**.  
This leads to:
- Increased patient waiting times  
- Poor resource utilization  
- Higher risk for critical patients  

---

## 💡 Solution Overview
We developed a **simulation-based Hospital Triage System** that uses intelligent decision-making to:

- Dynamically manage incoming patients  
- Prioritize patients based on severity  
- Allocate doctors efficiently  
- Compare baseline vs AI-driven strategies  

The system demonstrates how **AI can improve hospital workflow under real-world constraints**.

---

## ⚙️ Tech Stack

- **Language:** Python  
- **Simulation Engine:** Custom Environment  
- **AI Approach:** Heuristic-based (extendable to Reinforcement Learning)  
- **Architecture:** Modular (Environment + Simulator + Evaluation)

---

## 🧠 System Architecture
# 🏥 AI-Powered Hospital Triage System

## 🚨 Problem Statement
Emergency departments often suffer from **overcrowding, inefficient patient prioritization, and limited medical resources**.  
This leads to:
- Increased patient waiting times  
- Poor resource utilization  
- Higher risk for critical patients  

---

## 💡 Solution Overview
We developed a **simulation-based Hospital Triage System** that uses intelligent decision-making to:

- Dynamically manage incoming patients  
- Prioritize patients based on severity  
- Allocate doctors efficiently  
- Compare baseline vs AI-driven strategies  

The system demonstrates how **AI can improve hospital workflow under real-world constraints**.

---

## ⚙️ Tech Stack

- **Language:** Python  
- **Simulation Engine:** Custom Environment  
- **AI Approach:** Heuristic-based (extendable to Reinforcement Learning)  
- **Architecture:** Modular (Environment + Simulator + Evaluation)

---

## 🧠 System Architecture
- Patient Arrival → Queue → Triage Decision → Doctor Allocation → Treatment → Metrics Evaluation


### Components:
- **Environment (`hospital_triage_env_environment.py`)**
  - Simulates patients, queue, and doctors  
- **Simulator (`evaluation/simulator.py`)**
  - Runs episodes and compares strategies  
- **Evaluation (`run_eval.py`)**
  - Outputs performance metrics  

---

## 🔍 Key Features

### 1. Dynamic Patient Simulation
- Random patient arrivals  
- Severity-based classification (1–5 scale)  

### 2. Multi-Doctor Allocation
- Parallel patient handling  
- Real-time doctor availability tracking  

### 3. Intelligent Triage Strategy
- Baseline (random/FIFO)  
- AI Agent (severity-based prioritization)  

### 4. Performance Metrics
- Average queue length  
- Maximum wait time  
- Mortality tracking  
- Comparative analysis  

---

## 📊 Results

| Metric | Baseline | AI Agent |
|--------|--------|---------|
| Avg Queue Length | ~2.28 | ~2.14 |
| Queue Reduction | — | ✅ Improved |
| Mortality | 0 | 0 |

👉 The AI agent demonstrates **better queue management and resource utilization**.

---

## ▶️ How to Run

### 1. Clone Repository
```bash
git clone <your-repo-link>
cd OpenEnv_HospitalTriage

## Project Structure
OpenEnv_HospitalTriage/
│
├── hospital_triage_env_environment.py   # Core environment
├── evaluation/
│   ├── simulator.py                    # Simulation runner
│   └── metrics.py                      # Metrics tracking (optional)
│
├── run_eval.py                         # Entry point
├── README.md
└── requirements.txt