import QtQuick

Rectangle {
    id: clockScene

    width: 480
    height: 360
    color: "black"

    property string time: "--:--:--"
    property var digitPattern: ({
        "0": "01110"
           + "10001"
           + "10001"
           + "10001"
           + "10001"
           + "10001"
           + "01110",
        "1": "00100"
           + "01100"
           + "00100"
           + "00100"
           + "00100"
           + "00100"
           + "01110",
        "2": "01110"
           + "10001"
           + "00001"
           + "00010"
           + "00100"
           + "01000"
           + "11111",
        "3": "11110"
           + "00001"
           + "00001"
           + "01110"
           + "00001"
           + "00001"
           + "11110",
        "4": "00010"
           + "00110"
           + "01010"
           + "10010"
           + "11111"
           + "00010"
           + "00010",
        "5": "11111"
           + "10000"
           + "10000"
           + "11110"
           + "00001"
           + "00001"
           + "11110",
        "6": "01110"
           + "10000"
           + "10000"
           + "11110"
           + "10001"
           + "10001"
           + "01110",
        "7": "11111"
           + "00001"
           + "00010"
           + "00100"
           + "01000"
           + "01000"
           + "01000",
        "8": "01110"
           + "10001"
           + "10001"
           + "01110"
           + "10001"
           + "10001"
           + "01110",
        "9": "01110"
           + "10001"
           + "10001"
           + "01111"
           + "00001"
           + "00001"
           + "01110"
    })

    Text {
        text: clockScene.time
        color: "white"
        font.pixelSize: 28
        anchors.centerIn: parent
    }

    DotDigit {
        x: 20
        y: 20
        pattern: clockScene.digitPattern[clockScene.time[6]] || clockScene.blankPattern
    }

    DotDigit {
        x: 130
        y: 20
        pattern: clockScene.digitPattern[clockScene.time[7]] || clockScene.blankPattern
    }

    TapHandler {
        onTapped: (eventpoint, button) => console.log("Clock clicked")
    }

    property string blankPattern: "00000"
                                + "00000"
                                + "00000"
                                + "00000"
                                + "00000"
                                + "00000"
                                + "00000"

}
