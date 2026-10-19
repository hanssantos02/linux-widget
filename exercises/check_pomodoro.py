from timer_controller import TimerController

timer = TimerController(10, 4)

# timer.start()
# timer.update(10)
# timer.start()
# timer.update(4)

# assert timer.phase == "focus"
# assert timer.status == "ready"
# assert timer.remaining_time == 10

# timer.start()
# timer.update(3.25)
# timer.pause()

# assert timer.phase == "focus"
# assert timer.status == "paused"
# assert timer.remaining_time == 6.75

# timer.update(100)
# timer.start()
# timer.resume()
# timer.update(2.5)

# assert timer.phase == "focus"
# assert timer.status == "running"
# assert timer.remaining_time == 4.25

# timer.start()
# timer.update(10)
# timer.start()
# timer.update(1.25)
# timer.pause()

# assert timer.phase == "break"
# assert timer.status == "paused"
# assert timer.remaining_time == 2.75

# timer.update(100)
# timer.resume()
# timer.update(2.75)

# assert timer.phase == "focus"
# assert timer.status == "ready"
# assert timer.remaining_time == 10

# timer.pause()
# timer.resume()

# assert timer.phase == "focus"
# assert timer.status == "ready"
# assert timer.remaining_time == 10

timer.start()
timer.update(2)
timer.pause()
timer.pause()

assert timer.phase == "focus"
assert timer.status == "paused"
assert timer.remaining_time == 8

timer.resume()
timer.resume()

assert timer.phase == "focus"
assert timer.status == "running"
assert timer.remaining_time == 8

timer = TimerController(10, 4)

timer.start()
timer.update(5)
timer.reset()

assert timer.phase == "focus"
assert timer.status == "ready"
assert timer.remaining_time == 10

timer.update(5)

assert timer.phase == "focus"
assert timer.status == "ready"
assert timer.remaining_time == 10

timer = TimerController(10, 4)

timer.start()
timer.update(10)
timer.start()
timer.update(2)
timer.pause()
timer.reset()

assert timer.phase == "focus"
assert timer.status == "ready"
assert timer.remaining_time == 10
assert timer.focus_duration_seconds == 10
assert timer.break_duration_seconds == 4

timer = TimerController(10, 4)

timer.reset()

assert timer.phase == "focus"
assert timer.status == "ready"
assert timer.remaining_time == 10

timer = TimerController(10, 4)

timer.start()
timer.update(0.25)

assert timer.remaining_time == 9.75
assert timer.remaining_seconds == 10

timer.update(9.5)

assert timer.remaining_time == 0.25
assert timer.remaining_seconds == 1

timer.update(0.25)

assert timer.phase == "break"
assert timer.status == "ready"
assert timer.remaining_time == 4
assert timer.remaining_seconds == 4
assert timer.phase_duration_seconds == 4

timer.reset()

assert timer.phase == "focus"
assert timer.status == "ready"
assert timer.remaining_time == 10
assert timer.remaining_seconds == 10
assert timer.phase_duration_seconds == 10
print("All Pomodoro checks passed")
