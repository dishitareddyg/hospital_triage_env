import requests
from agent.inference import choose_action

BASE_URL = "http://127.0.0.1:8000"


def validate_environment():
    issues = []

    try:
        res = requests.post(f"{BASE_URL}/reset", json={})
        res.raise_for_status()
    except Exception as e:
        return {"status": "FAIL", "issues": [f"Reset failed: {e}"]}

    data = res.json()
    observation = data.get("observation", {}).get("data", {})

    steps = 20

    for i in range(steps):
        try:
            action = choose_action(observation)

            res = requests.post(
                f"{BASE_URL}/step",
                json={"action": action}
            )
            res.raise_for_status()

            result = res.json()

            # Validate structure
            if "observation" not in result:
                issues.append("Missing observation")

            if "reward" not in result:
                issues.append("Missing reward")

            if "done" not in result:
                issues.append("Missing done flag")

            observation = result["observation"]["data"]

        except Exception as e:
            issues.append(f"Step {i} failed: {str(e)}")
            break

    if issues:
        return {"status": "FAIL", "issues": issues}

    return {"status": "PASS", "issues": []}


if __name__ == "__main__":
    result = validate_environment()
    print("\nVALIDATION RESULT:", result)