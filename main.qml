import QtQuick

Rectangle {
    id: clockScene

    width: 480
    height: 360
    color: "black"

    property string time: "--:--:--"
    property string previewCharacter: "3"

    TapHandler {
        onTapped: (eventpoint, button) => console.log("Clock clicked")
    }

    FlipCharacter {
        id: previewTile

        character: clockScene.previewCharacter
        anchors.centerIn: parent
    }

    Rectangle {
        width: 140
        height: 40
        radius: 4
        color: "#303030"
        anchors.left: previewTile.right
        anchors.leftMargin: 16
        anchors.verticalCenter: parent.verticalCenter

        Text {
            anchors.centerIn: parent
            color: "white"
            font.pixelSize: 16
            text: "Target: " + clockScene.previewCharacter
        }

        TapHandler {
            onTapped: (eventpoint, button) => {
                clockScene.previewCharacter = clockScene.previewCharacter === "3" ? "4" : "3"
            }
        }
    }
}
