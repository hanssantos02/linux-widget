from PySide6.QtCore import QSize, QTimer, QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQuick import QQuickView


def request_rollover():
    root = window.rootObject()
    root.setProperty("time", "12:00:00 AM")


def request_latest():
    root = window.rootObject()
    root.setProperty("time", "12:00:03 AM")


app = QGuiApplication()
window = QQuickView()
qml_url = QUrl.fromLocalFile("/home/hans/repos/linux-widget/main.qml")
initial_values = {"time": "11:59:59 PM"}

window.setResizeMode(QQuickView.ResizeMode.SizeRootObjectToView)
window.setInitialProperties(initial_values)
window.setSource(qml_url)
window.setTitle("Split-flap rollover check")
window.setMinimumSize(QSize(1100, 240))
window.show()
timer = QTimer()
timer.singleShot(2000, request_rollover)
timer.singleShot(2200, request_latest)
timer.singleShot(6000, app.quit)
app.exec()
