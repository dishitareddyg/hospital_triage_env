from typing import List
import random

from openenv.core import Environment
from hospital_triage_env.models import (
    HospitalTriageObservation,
    HospitalTriageAction,
    Patient
)


class HospitalTriageEnvironment(Environment):

    def __init__(self):
        super().__init__()

        self.patients: List[Patient] = []
        self.max_doctors = 2
        self.available_doctors = 2

        self.time_step = 0
        self.done = False
        self.patient_counter = 0

        # metrics
        self.total_deaths = 0
        self.total_treated = 0

    # ---------------------------
    # RESET
    # ---------------------------
    def reset(self, episode_id=None, seed=None):

        if seed:
            random.seed(seed)

        self.time_step = 0
        self.done = False
        self.available_doctors = self.max_doctors
        self.patient_counter = 0
        self.total_deaths = 0
        self.total_treated = 0

        self.patients = []

        for _ in range(5):
            self._add_patient()

        return self._obs(0.0)

    async def reset_async(self, episode_id=None, seed=None):
        return self.reset(episode_id, seed)

    # ---------------------------
    # STEP
    # ---------------------------
    def step(self, action: HospitalTriageAction):

        self.time_step += 1
        reward = 0.0

        # doctors reset
        self.available_doctors = self.max_doctors

        # ---------------------------
        # PROCESS ONGOING TREATMENTS
        # ---------------------------
        still_active = []

        for p in self.patients:

            if p.status == "in_treatment":
                p.treatment_time_left -= 1

            if p.treatment_time_left <= 0:
                self.total_treated += 1
                reward += 2.0 * p.severity
                continue  # patient leaves

            still_active.append(p)

        self.patients = still_active

        # ---------------------------
        # APPLY ACTION (START TREATMENT)
        # ---------------------------
        if action.action_type == "assign" and action.patient_id:

            for p in self.patients:
                if p.id == action.patient_id and p.status == "waiting":

                    if self.available_doctors > 0:
                        p.status = "in_treatment"

                    # treatment takes time (critical patients take longer)
                    p.treatment_time_left = int(3 + p.severity * 5)

                    self.available_doctors -= 1
                break

        # ---------------------------
        # UPDATE WAITING PATIENTS
        # ---------------------------
        updated_patients = []

        for p in self.patients:

            if p.status == "waiting":
                p.waiting_time += 1
                p.severity = min(1.0, p.severity + 0.07)

            reward -= 0.2 * p.waiting_time  # stronger penalty

            if p.severity >= 1.0:
                self.total_deaths += 1
                reward -= 10.0
                continue

            updated_patients.append(p)

        self.patients = updated_patients

        # ---------------------------
        # NEW ARRIVALS (HEAVIER LOAD)
        # ---------------------------
        arrivals = random.choices([1, 2, 3, 4],weights=[0.2, 0.4, 0.3, 0.1])[0]

        for _ in range(arrivals):
            self._add_patient()

        # ---------------------------
        # DONE
        # ---------------------------
        if self.time_step >= 50:
            self.done = True

        return self._obs(reward)

    # ---------------------------
    def _add_patient(self):
        self.patient_counter += 1

        self.patients.append(
            Patient(
                id=self.patient_counter,
                severity=round(random.uniform(0.3, 0.9), 2),
                waiting_time=0,
                status="waiting"
            )
        )

    # ---------------------------
    def _obs(self, reward):
        return HospitalTriageObservation(
            status="running",
            data={
                "patients": [p.model_dump() for p in self.patients],
                "available_doctors": self.available_doctors,
                "time_step": self.time_step,
                "deaths": self.total_deaths,
                "treated": self.total_treated
            },
            reward=reward,
            done=self.done
        )

    def state(self):
        return self._obs(0.0)

    def close(self):
        pass