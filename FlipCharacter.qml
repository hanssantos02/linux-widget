import QtQuick

Rectangle {
    id: flipTile

    width: 120
    height: 160
    radius: 8
    color: "#202020"

    property string character: " "

    Item {
        id: upperHalf

        width: flipTile.width
        height: flipTile.height / 2
        x: 0
        y: 0
        clip: true

        Text {
            x: 0
            y: 0
            width: flipTile.width
            height: flipTile.height
            text: flipTile.character
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            color: "white"
            font.pixelSize: 112
            font.bold: true
        }
    }

    Item {
        id: lowerHalf

        width: flipTile.width
        height: flipTile.height / 2
        x: 0
        y: flipTile.height / 2
        clip: true

        Text {
            x: 0
            y: -parent.height
            width: flipTile.width
            height: flipTile.height
            text: flipTile.character
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            color: "white"
            font.pixelSize: 112
            font.bold: true
        }
    }

    Rectangle {
        width: flipTile.width
        height: 2
        x: 0
        y: flipTile.height / 2 - height / 2
        color: "#080808"
        z: 1
    }
}
