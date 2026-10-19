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

    Column {
        anchors.centerIn: parent
        spacing: 16

        Row {
            spacing: 12

            Repeater {
                model: 8
                delegate: FlipCharacter {
                    required property int index
                    character: clockScene.time[index]
                }
            }
        }

        Text {
            anchors.horizontalCenter: parent.horizontalCenter

            color: "white"
            text: clockScene.time
            font.pixelSize: 18
        }
    }
}
