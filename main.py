from datetime import datetime

from PySide6.QtCore import QTimer, QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQuick import QQuickView

from exercises.clock_format import format_time

use_24_hour = False
refresh_interval_ms = 1000

def announce_ready():
    date = datetime.now()
    date_format = format_time(date, use_24_hour)
    print(date_format)
    root = window.rootObject()
    root.setProperty("time", date_format)

app = QGuiApplication()
window = QQuickView()
qml_url = QUrl.fromLocalFile("/home/hans/repos/linux-widget/main.qml")
initial_values = {"time": format_time(datetime.now(), use_24_hour)}

window.setResizeMode(QQuickView.ResizeMode.SizeRootObjectToView)
window.setInitialProperties(initial_values)
window.setSource(qml_url)
window.setTitle("test")
window.show()
timer = QTimer()
timer.timeout.connect(announce_ready)
timer.start(refresh_interval_ms)
app.exec()
