from PySide6.QtCore import Qt ,QTimer, QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQuick import QQuickView

def announce_ready():
    print("Timer fired")
    root = window.rootObject()
    root.setProperty("airportCode", "MNL")

app = QGuiApplication()
window = QQuickView()
qml_url = QUrl.fromLocalFile("/home/hans/repos/linux-widget/experiments/desktop_probe.qml")
initial_values = {"airportCode": "DVO"}

window.setResizeMode(QQuickView.ResizeMode.SizeRootObjectToView)
window.setInitialProperties(initial_values)
window.setSource(qml_url)
window.setTitle("Desktop Experiment")
window.setPosition(40, 60)
window.setFlag(Qt.WindowType.WindowTransparentForInput, True)
window.setFlag(Qt.WindowType.FramelessWindowHint, True)
window.setFlag(Qt.WindowType.WindowDoesNotAcceptFocus, True)
QTimer.singleShot(5000, window.show)
QTimer.singleShot(10000, announce_ready)
QTimer.singleShot(30000, app.quit)
app.exec()
