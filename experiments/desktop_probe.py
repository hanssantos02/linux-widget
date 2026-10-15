from PySide6.QtCore import QTimer, QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQuick import QQuickView

def announce_ready():
    print("Timer fired")
    root = window.rootObject()
    root.setProperty("airportCode", "MNL")

app = QGuiApplication()
window = QQuickView()
qml_url = QUrl.fromLocalFile("/home/hans/repos/linux-widget/main.qml")
initial_values = {"airportCode": "DVO"}

window.setResizeMode(QQuickView.ResizeMode.SizeRootObjectToView)
window.setInitialProperties(initial_values)
window.setSource(qml_url)
window.setTitle("Desktop Experiment")
window.show()
QTimer.singleShot(5000, announce_ready)
app.exec()
