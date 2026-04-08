from pydantic import BaseModel
from typing import Dict, Any, Literal


class Patient(BaseModel):
    id: int
    severity: float
    waiting_time: int
    status: Literal["waiting", "in_treatment"]
    treatment_time_left: int = 0


class HospitalTriageObservation(BaseModel):
    status: str
    data: Dict[str, Any]
    reward: float = 0.0
    done: bool = False


class HospitalTriageAction(BaseModel):
    action_type: Literal["assign", "wait"]
    patient_id: int | None = None