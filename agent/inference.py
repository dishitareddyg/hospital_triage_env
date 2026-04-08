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