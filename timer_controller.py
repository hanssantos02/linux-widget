import math

class TimerController:
    def __init__(self, focus_duration_seconds=1500, break_duration_seconds=300):
        self.focus_duration_seconds = focus_duration_seconds
        self.break_duration_seconds = break_duration_seconds
        self.phase = "focus"
        self.status = "ready"
        self.remaining_time = self.focus_duration_seconds

    def start(self):
        if self.status == "ready":
            self.status = "running"

    def update(self, elapsed_seconds):
        if self.status != "running":
            return
        self.remaining_time -= elapsed_seconds
        if self.remaining_time <= 0:
            self.phase = "break" if self.phase == "focus" else "focus"
            self.status = "ready"
            self.remaining_time = (
                self.break_duration_seconds
                if self.phase == "break"
                else self.focus_duration_seconds
            )

    def pause(self):
        if self.status != "running":
            return
        self.status = "paused"

    def resume(self):
        if self.status != "paused":
            return
        self.status = "running"

    def reset(self):
        self.phase = "focus"
        self.status = "ready"
        self.remaining_time = self.focus_duration_seconds

    @property
    def remaining_seconds(self):
        return max(0, math.ceil(self.remaining_time))

    @property
    def phase_duration_seconds(self):
        return (
            self.focus_duration_seconds
            if self.phase == "focus"
            else self.break_duration_seconds
        )
