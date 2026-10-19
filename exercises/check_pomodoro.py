from timer_controller import TimerController

timer = TimerController(10, 4)

timer.start()
timer.update(10)
timer.start()
timer.update(4)

assert timer.phase == "focus"
assert timer.status == "ready"
assert timer.remaining_time == 10
print("All Pomodoro checks passed")
