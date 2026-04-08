import os
from openai import OpenAI
from hospital_triage_env import HospitalTriageEnv

client = OpenAI(
    base_url=os.getenv("API_BASE_URL"),
    api_key=os.getenv("OPENAI_API_KEY"),
)

MODEL = os.getenv("MODEL_NAME")
HF_TOKEN = os.getenv("HF_TOKEN")

def run():
    env = HospitalTriageEnv()
    obs = env.reset()

    print("[START]")

    done = False
    step = 0

    while not done:
        prompt = f"""
        You are a hospital triage agent.
        Current queue: {obs}
        Decide action: assign patients to doctors or wait.
        """

        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
        )

        action = response.choices[0].message.content

        obs, reward, done, info = env.step(action)

        print(f"[STEP] step={step} action={action} reward={reward}")

        step += 1

    print("[END]")

if __name__ == "__main__":
    run()

def choose_action(state):

    patients = state.get("patients", [])

    if not patients:
        return {"action_type": "wait", "patient_id": None}

    # prioritize CRITICAL + long waiting
    patients.sort(
        key=lambda p: (p["severity"] * 2 + p["waiting_time"]),
        reverse=True
    )

    return {
        "action_type": "assign",
        "patient_id": patients[0]["id"]
    }