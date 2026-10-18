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
        character: "4"
        anchors.centerIn: parent
    }
}
