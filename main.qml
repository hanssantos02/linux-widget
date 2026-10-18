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
            delegate: Dot {
                required property int index
                property int rowIndex: Math.floor(index / digitGrid.columns)
                property int columnIndex: index % digitGrid.columns
                lit: digitGrid.pattern[index] === "1"
            }
        }
        id: digitGrid
        property var pattern:   "01110"
                              + "10001"
                              + "10001"
                              + "10001"
                              + "10001"
                              + "10001"
                              + "01110"
    }


    TapHandler {
        onTapped: (eventpoint, button) => console.log("Clock clicked")
    }

    property string time: "--:--:--"
}
