from PySide6.QtCore import QCoreApplication

from timer_bridge import TimerBridge
from timer_controller import TimerController


app = QCoreApplication([])
bridge = TimerBridge()
assert bridge.phase == "focus"
assert bridge.status == "ready"
assert bridge.remainingSeconds == 1500
assert bridge.phaseDurationSeconds== 1500
assert bridge.focusDurationSeconds == 1500
assert bridge.breakDurationSeconds == 300

controller = TimerController(10, 4)
bridge = TimerBridge(controller)

assert bridge.phase == "focus"
assert bridge.status == "ready"
assert bridge.remainingSeconds == 10
assert bridge.phaseDurationSeconds == 10
assert bridge.focusDurationSeconds == 10
assert bridge.breakDurationSeconds== 4

controller = TimerController(10, 4)
controller.start()
controller.update(2.5)
controller.pause()
bridge = TimerBridge(controller)

assert bridge.phase == "focus"
assert bridge.status == "paused"
assert bridge.remainingSeconds == 8
assert bridge.phaseDurationSeconds == 10
assert controller.remaining_time == 7.5

controller = TimerController(10, 4)
controller.start()
controller.update(10)
bridge = TimerBridge(controller)

assert bridge.phase == "break"
assert bridge.status == "ready"
assert bridge.remainingSeconds == 4
assert bridge.phaseDurationSeconds == 4
assert bridge.focusDurationSeconds == 10
assert bridge.breakDurationSeconds == 4


controller = TimerController(10, 4)
bridge = TimerBridge(controller)
observed = []

bridge._publish_state()

controller.start()
bridge._publish_state()

controller.update(0.25)
bridge._publish_state()

controller.update(0.75)
bridge._publish_state()

controller.update(9)
bridge._publish_state()

bridge._publish_state()

controller.reset()
bridge._publish_state()


clock_state = {"now": 0.0}

def fake_clock():
    return clock_state["now"]


clock_state["now"] = 0.0
controller = TimerController(10, 4)
bridge = TimerBridge(controller, clock=fake_clock)
observed = []
def record_state():
    observed.append((
        bridge.phase,
        bridge.status,
        bridge.remainingSeconds,
        bridge.phaseDurationSeconds
    ))
bridge.stateChanged.connect(record_state)

clock_state["now"] = 0
bridge.start()

assert bridge.phase == "focus"
assert bridge.status == "running"
assert bridge.remainingSeconds == 10
assert bridge.phaseDurationSeconds == 10
assert len(observed) == 1
assert observed[-1] == ("focus", "running", 10, 10)

clock_state["now"] = 10
bridge.pause()

assert bridge.phase == "break"
assert bridge.status == "ready"
assert bridge.remainingSeconds == 4
assert bridge.phaseDurationSeconds == 4
assert len(observed) == 2
assert observed[-1] == ("break", "ready", 4, 4)

clock_state["now"] = 10
bridge.resume()

assert bridge.phase == "break"
assert bridge.status == "ready"
assert bridge.remainingSeconds == 4
assert bridge.phaseDurationSeconds == 4
assert len(observed) == 2
assert observed[-1] == ("break", "ready", 4, 4)

clock_state["now"] = 10
bridge.start()

assert bridge.phase == "break"
assert bridge.status == "running"
assert bridge.remainingSeconds == 4
assert bridge.phaseDurationSeconds == 4
assert len(observed) == 3
assert observed[-1] == ("break", "running", 4, 4)

clock_state["now"] = 15
bridge.start()

assert bridge.phase == "focus"
assert bridge.status == "running"
assert bridge.remainingSeconds == 10
assert bridge.phaseDurationSeconds == 10
assert len(observed) == 4
assert observed[-1] == ("focus", "running", 10, 10)

clock_state["now"] = 25
bridge.reset()

assert bridge.phase == "focus"
assert bridge.status == "ready"
assert bridge.remainingSeconds == 10
assert bridge.phaseDurationSeconds == 10
assert len(observed) == 5
assert observed[-1] == ("focus", "ready", 10, 10)

clock_state["now"] = 25
bridge.reset()

assert bridge.phase == "focus"
assert bridge.status == "ready"
assert bridge.remainingSeconds == 10
assert bridge.phaseDurationSeconds == 10
assert len(observed) == 5
assert observed[-1] == ("focus", "ready", 10, 10)

print("pass")
