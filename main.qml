import QtQuick

Rectangle {
    id: clockScene

    width: 1100
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
                delegate: Item {
                    id: characterContainer
                    required property int index
                    readonly property bool isSeparator: index === 2 || index === 5

                    width: isSeparator ? 24 : flipCharacter.width
                    height: flipCharacter.height

                    FlipCharacter {
                        id: flipCharacter
                        visible: !characterContainer.isSeparator
                        character: clockScene.time[characterContainer.index]
                    }

                    Text {
                        anchors.centerIn: parent
                        visible: characterContainer.isSeparator
                        text: ":"
                        color: "#b8b8b8"
                        font.pixelSize: 64
                    }
                }
            }
        }

        Text {
            anchors.horizontalCenter: parent.horizontalCenter

            color: "#b8b8b8"
            text: clockScene.time.slice(9)
            font.pixelSize: 18
            visible: text.length > 0
        }
    }
}
