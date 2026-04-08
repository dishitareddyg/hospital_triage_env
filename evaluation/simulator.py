import requests
import random

from inference import choose_action
from evaluation.metrics import MetricsTracker

BASE_URL = "http://127.0.0.1:8000"


# -----------------------------
# API CALLS
# -----------------------------
def reset_env():
    res = requests.post(f"{BASE_URL}/reset", json={})
    res.raise_for_status()
    return res.json()


def step_env(action):
    res = requests.post(
        f"{BASE_URL}/step",
        json={"action": action}
    )
    res.raise_for_status()
    return res.json()


# -----------------------------
# BASELINE AGENT (SMART RANDOM)
# -----------------------------
def random_agent(state):
    patients = state.get("patients", [])
    available_doctors = state.get("available_doctors", 0)

    waiting = [p for p in patients if p["status"] == "waiting"]

    if not waiting or available_doctors == 0:
        return {"action_type": "wait", "patient_id": None}

    # Slightly biased random (not fully dumb)
    chosen = random.choice(waiting)

    return {
        "action_type": "assign",
        "patient_id": chosen["id"]
    }


# -----------------------------
# RUN SIMULATION
# -----------------------------
def run_simulation(agent_fn, label="Agent", max_steps=50):
    print(f"\n===== RUNNING: {label} =====")

    data = reset_env()
    observation = data["observation"]["data"]

    metrics = MetricsTracker()
    total_reward = 0

    for step in range(max_steps):

        action = agent_fn(observation)

        try:
            result = step_env(action)
        except Exception as e:
            print(f"❌ Step {step} failed:", e)
            break

        obs = result.get("observation", {})
        observation = obs.get("data", {})

        reward = result.get("reward", 0)
        done = result.get("done", False)

        total_reward += reward

        # Update metrics (IMPORTANT)
        metrics.update(observation)

        print(
            f"Step {step:02d} | "
            f"Reward: {round(reward, 2):>6} | "
            f"Queue: {len(observation.get('patients', []))} | "
            f"Doctors: {observation.get('available_doctors')} | "
            f"Done: {done}"
        )

        if done:
            break

    final_metrics = metrics.compute()

    print("\n--- RESULTS ---")
    for k, v in final_metrics.items():
        print(f"{k}: {v}")

    print("Total Reward:", round(total_reward, 2))

    return final_metrics


# -----------------------------
# MAIN EXECUTION
# -----------------------------
if __name__ == "__main__":

    print("\n==============================")
    print("HOSPITAL TRIAGE SIMULATION")
    print("==============================")

    # Baseline
    baseline_metrics = run_simulation(
        random_agent,
        label="Baseline (Random)"
    )

    # AI Agent
    ai_metrics = run_simulation(
        choose_action,
        label="AI Agent (Heuristic)"
    )

    # -----------------------------
    # COMPARISON
    # -----------------------------
    print("\n==============================")
    print("FINAL COMPARISON")
    print("==============================")

    print("\nBaseline:", baseline_metrics)
    print("AI Agent:", ai_metrics)

    print("\nKEY METRICS:")

    print(f"Avg Wait ↓: {baseline_metrics['avg_wait_time']} → {ai_metrics['avg_wait_time']}")
    print(f"Queue ↓: {baseline_metrics['avg_queue_length']} → {ai_metrics['avg_queue_length']}")
    print(f"Mortality ↓: {baseline_metrics['mortality_rate']} → {ai_metrics['mortality_rate']}")

    improvement = baseline_metrics['avg_wait_time'] - ai_metrics['avg_wait_time']
    print("\nImprovement (Wait Time):", round(improvement, 2))