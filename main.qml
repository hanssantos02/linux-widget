import QtQuick

Rectangle {
    width: 480
    height: 240
    color: "black"

    Text {
        text: parent.time
        color: "white"
        font.pixelSize: 28
        anchors.centerIn: parent
    }

    TapHandler {
        onTapped: (eventpoint, button) => console.log("Clock clicked")
    }

    property string time: "--:--:--"
}
