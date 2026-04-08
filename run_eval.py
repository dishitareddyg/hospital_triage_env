from evaluation.simulator import run_simulation
from evaluation.validator import validate_environment
from agent.inference import choose_action
import random


def random_agent(state):
    patients = state.get("patients", [])
    if not patients:
        return {"action_type": "wait", "patient_id": None}

    p = random.choice(patients)
    return {"action_type": "assign", "patient_id": p["id"]}


if __name__ == "__main__":

    print("\n==============================")
    print("HOSPITAL TRIAGE EVALUATION")
    print("==============================")

    print("\nRunning validation...")
    val = validate_environment()

    if val["status"] != "PASS":
        print("VALIDATION FAILED:", val["issues"])
        exit()

    print("Validation passed")

    baseline = run_simulation(random_agent, "Baseline")
    ai = run_simulation(choose_action, "AI Agent")

    print("\n==============================")
    print("FINAL COMPARISON")
    print("==============================")

    print("\nBaseline:", baseline)
    print("AI Agent:", ai)

    print("\nKEY RESULT:")
    print("Wait Time Improvement:", baseline["avg_wait_time"] - ai["avg_wait_time"])
    print("Queue Reduction:", baseline["avg_queue_length"] - ai["avg_queue_length"])