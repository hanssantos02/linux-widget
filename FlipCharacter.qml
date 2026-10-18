import QtQuick

Rectangle {
    id: flipTile

    width: 120
    height: 160
    radius: 8
    color: "#202020"

    property string character: " "

    Text {
        text: flipTile.character
        anchors.fill: parent
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        color: "white"
        font.pixelSize: 112
        font.bold: true
    }
}
