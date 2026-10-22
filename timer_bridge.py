from time import monotonic

from PySide6.QtCore import QObject, Property, Signal

from timer_controller import TimerController


class TimerBridge(QObject):
    stateChanged = Signal()

    def __init__(self, controller=None, parent=None, clock=monotonic):
        super().__init__(parent)

        if controller is None:
            controller = TimerController()
        self._controller = controller
        self._snapshot = self._read_state()
        self._clock = clock
        self._last_reading = self._clock()

    def _read_state(self):
        return {
            "phase": self._controller.phase,
            "status": self._controller.status,
            "remainingSeconds": self._controller.remaining_seconds,
            "phaseDurationSeconds": self._controller.phase_duration_seconds,
            "focusDurationSeconds": self._controller.focus_duration_seconds,
            "breakDurationSeconds": self._controller.break_duration_seconds,
        }

    def _publish_state(self):
        state = self._read_state()
        if self._snapshot == state:
            return
        self._snapshot = state
        self.stateChanged.emit()

    def _sync_elapsed(self):
        now = self._clock()
        elapsed = now - self._last_reading
        self._last_reading = now
        self._controller.update(elapsed)

    def refresh(self):
        self._sync_elapsed()
        self._publish_state()


    @Property(str, notify=stateChanged)
    def phase(self):
        return self._snapshot["phase"]

    @Property(str, notify=stateChanged)
    def status(self):
        return self._snapshot["status"]

    @Property(int, notify=stateChanged)
    def remainingSeconds(self):
        return self._snapshot["remainingSeconds"]

    @Property(int, notify=stateChanged)
    def phaseDurationSeconds(self):
        return self._snapshot["phaseDurationSeconds"]

    @Property(int, notify=stateChanged)
    def focusDurationSeconds(self):
        return self._snapshot["focusDurationSeconds"]

    @Property(int, notify=stateChanged)
    def breakDurationSeconds(self):
        return self._snapshot["breakDurationSeconds"]
