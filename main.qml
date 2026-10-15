import QtQuick

Rectangle {
    width: 480
    height: 240
    color: "black"

    Text {
        text: "Airport: " + parent.airportCode
        color: "white"
        font.pixelSize: 28
        anchors.centerIn: parent
    }

    TapHandler {
        onTapped: (eventpoint, button) => console.log("Clock clicked")
    }

    property string airportCode: "CEB"
}
