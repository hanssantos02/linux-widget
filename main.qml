import QtQuick

Rectangle {
    width: 480
    height: 360
    color: "black"

    Text {
        text: parent.time
        color: "white"
        font.pixelSize: 28
        anchors.centerIn: parent
    }

    DotDigit {
        x: 20
        y: 20
        pattern: "01110"
               + "10001"
               + "10001"
               + "10001"
               + "10001"
               + "10001"
               + "01110"
    }

    DotDigit {
        x: 130
        y: 20
        pattern: "11111"
               + "11111"
               + "11111"
               + "11111"
               + "11111"
               + "11111"
               + "11111"
    }

    TapHandler {
        onTapped: (eventpoint, button) => console.log("Clock clicked")
    }

    property string time: "--:--:--"
}
