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

    Grid {
        x: 20
        y: 20
        columns: 5
        spacing: 4
        Repeater {
            model: 35
            delegate: Dot {}
        }
    }


    TapHandler {
        onTapped: (eventpoint, button) => console.log("Clock clicked")
    }

    property string time: "--:--:--"
}
