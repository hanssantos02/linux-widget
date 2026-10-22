from PySide6.QtCore import QObject, Property, Signal

from timer_controller import TimerController


class TimerBridge(QObject):
    stateChanged = Signal()

    def __init__(self, controller=None, parent=None):
        super().__init__(parent)

        if controller is None:
            controller = TimerController()
        self._controller = controller
        self._snapshot = self._read_state()

    def _read_state(self):
        return {
            "phase": self._controller.phase,
            "status": self._controller.status,
            "remainingSeconds": self._controller.remaining_seconds,
            "phaseDurationSeconds": self._controller.phase_duration_seconds,
            "focusDurationSeconds": self._controller.focus_duration_seconds,
            "breakDurationSeconds": self._controller.break_duration_seconds,
        }

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
