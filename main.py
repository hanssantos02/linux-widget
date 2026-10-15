from PySide6.QtCore import QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQuick import QQuickView

app = QGuiApplication()
window = QQuickView()
qml_url = QUrl.fromLocalFile("/home/hans/repos/linux-widget/main.qml")

window.setResizeMode(QQuickView.ResizeMode.SizeRootObjectToView)
window.setSource(qml_url)
window.setTitle("test")
window.show()
app.exec()
