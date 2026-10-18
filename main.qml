import QtQuick

Rectangle {
    id: clockScene

    width: 480
    height: 360
    color: "black"

    property string time: "--:--:--"

    TapHandler {
        onTapped: (eventpoint, button) => console.log("Clock clicked")
    }

    FlipCharacter {
        id: previewTile

        character: clockScene.time[7]
        anchors.centerIn: parent
    }

    Text {
        color: "white"
        text: clockScene.time
        font.pixelSize: 18

        anchors.top: previewTile.bottom
        anchors.topMargin: 16
        anchors.horizontalCenter: parent.horizontalCenter
    }
}
