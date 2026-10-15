from PySide6.QtGui import QGuiApplication
from PySide6.QtQuick import QQuickWindow

app = QGuiApplication()
window = QQuickWindow()
window.resize(480, 240)
window.setTitle("test")
window.show()
app.exec()
