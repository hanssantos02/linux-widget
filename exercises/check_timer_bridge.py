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

def record_state():
    observed.append((
        bridge.phase,
        bridge.status,
        bridge.remainingSeconds,
        bridge.phaseDurationSeconds,
        bridge.focusDurationSeconds,
        bridge.breakDurationSeconds
    ))

bridge.stateChanged.connect(record_state)

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

controller = TimerController(10, 4)
bridge = TimerBridge(controller, clock=fake_clock)
observed = []
assert bridge.phase == "focus"
assert bridge.status == "ready"
assert bridge.remainingSeconds == 10
assert len(observed) == 0
bridge._publish_state()
print("pass")
