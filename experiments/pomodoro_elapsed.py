from time import monotonic
from PySide6.QtCore import QCoreApplication, QTimer
from timer_controller import TimerController

app = QCoreApplication([])
timer = TimerController(10, 4)

def refresh():
    global last_reading

    now = monotonic()
    elapsed_seconds = now - last_reading
    last_reading = now

    timer.update(elapsed_seconds)

    print(
        timer.phase,
        timer.status,
        timer.remaining_seconds
    )

def pause_now():
    refresh()
    timer.pause()
    print(
        timer.phase,
        timer.status,
        timer.remaining_seconds
    )

def resume_now():
    refresh()
    timer.resume()
    print(
        timer.phase,
        timer.status,
        timer.remaining_seconds
    )

last_reading = monotonic()
timer.start()
print(
    timer.phase,
    timer.status,
    timer.remaining_seconds
)

refresh_timer = QTimer()
refresh_timer.timeout.connect(refresh)
refresh_timer.start(1000)

refresh_timer.singleShot(2000, pause_now)
refresh_timer.singleShot(5000, resume_now)
refresh_timer.singleShot(16000, app.quit)
app.exec()
