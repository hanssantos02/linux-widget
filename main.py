from datetime import datetime

from PySide6.QtCore import QTimer, QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQuick import QQuickView

from exercises.clock_format import format_time


def announce_ready():
    date = datetime.now()
    print(format_time(date))
    root = window.rootObject()
    root.setProperty("airportCode", "MNL")

app = QGuiApplication()
window = QQuickView()
qml_url = QUrl.fromLocalFile("/home/hans/repos/linux-widget/main.qml")
initial_values = {"airportCode": "DVO"}

window.setResizeMode(QQuickView.ResizeMode.SizeRootObjectToView)
window.setInitialProperties(initial_values)
window.setSource(qml_url)
window.setTitle("test")
window.show()
timer = QTimer()
timer.timeout.connect(announce_ready)
timer.start(1000)
app.exec()
