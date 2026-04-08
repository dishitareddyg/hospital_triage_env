class MetricsTracker:
    def __init__(self):
        self.total_wait = 0
        self.total_patients = 0
        self.max_wait = 0
        self.queue_lengths = []
        self.deaths = 0

    def update(self, state):
        patients = state.get("patients", [])

        self.queue_lengths.append(len(patients))

        for p in patients:
            wt = p["waiting_time"]
            self.total_wait += wt
            self.total_patients += 1
            self.max_wait = max(self.max_wait, wt)

        self.deaths = state.get("deaths", self.deaths)

    def compute(self):

        avg_wait = self.total_wait / self.total_patients if self.total_patients else 0
        avg_queue = sum(self.queue_lengths) / len(self.queue_lengths)

        return {
            "avg_wait_time": round(avg_wait, 2),
            "max_wait_time": self.max_wait,
            "avg_queue_length": round(avg_queue, 2),
            "mortality": self.deaths
        }