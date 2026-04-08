import asyncio
import os
from typing import List, Optional
from openai import OpenAI
from hospital_triage_env import HospitalTriageEnv

API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL") or "https://router.huggingface.co/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"
# IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")
TASK_NAME = os.getenv("TASK_NAME", "hospital_triage")
BENCHMARK = os.getenv("BENCHMARK", "hospital_triage_env")
MAX_STEPS = 20

def log_start(task, env, model):
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step, action, reward, done, error):
    error_val = error if error else "null"
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error_val}", flush=True)

def log_end(success, steps, score, rewards):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True)

def get_action(client, obs):
    prompt = f"""
You are a hospital triage agent.
Current queue: {obs}
Decide action: assign patients to doctors or wait.
Respond with only the action string, no explanation.
"""
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
        )
        return (completion.choices[0].message.content or "wait").strip()
    except Exception as e:
        print(f"[DEBUG] Model error: {e}", flush=True)
        return "wait"

async def main():
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    env = HospitalTriageEnv()

    rewards: List[float] = []
    steps_taken = 0
    score = 0.0
    success = False

    log_start(task=TASK_NAME, env=BENCHMARK, model=MODEL_NAME)

    try:
        obs = env.reset()
        done = False

        for step in range(1, MAX_STEPS + 1):
            if done:
                break

            action = get_action(client, obs)
            obs, reward, done, info = env.step(action)
            error = info.get("error", None) if isinstance(info, dict) else None

            rewards.append(reward)
            steps_taken = step

            log_step(step=step, action=action, reward=reward, done=done, error=error)

        total_reward = sum(rewards)
        score = min(max(total_reward / MAX_STEPS, 0.0), 1.0)
        success = score > 0.1

    finally:
        try:
            env.close()
        except Exception as e:
            print(f"[DEBUG] env.close() error: {e}", flush=True)
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)

if _name_ == "_main_":
    asyncio.run(main())