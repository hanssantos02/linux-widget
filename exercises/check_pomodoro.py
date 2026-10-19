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
print("All Pomodoro checks passed")
