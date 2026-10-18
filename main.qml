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

    Dot {
        x: 20
        y: 20
        lit: true
    }

    Dot {
        x: 44
        y: 20
        lit: false
    }

    TapHandler {
        onTapped: (eventpoint, button) => console.log("Clock clicked")
    }

    property string time: "--:--:--"
}
