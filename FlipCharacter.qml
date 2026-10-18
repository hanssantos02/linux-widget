import QtQuick

Rectangle {
    id: flipTile

    property string character: " "
    property string displayedCharacter: "3"

    width: 120
    height: 160
    radius: 8
    color: "#202020"

    // Static upper half showing the next character.
    Item {
        id: upperBack

        x: 0
        y: 0
        z: 0
        width: flipTile.width
        height: flipTile.height / 2
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

    // Animated upper half showing the current character.
    Item {
        id: upperHalf

        x: 0
        y: 0
        z: 2
        width: flipTile.width
        height: flipTile.height / 2
        clip: true

        Rectangle {
            anchors.fill: parent
            color: flipTile.color
            radius: flipTile.radius
        }

        Text {
            x: 0
            y: 0
            width: flipTile.width
            height: flipTile.height
            text: flipTile.displayedCharacter
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            color: "white"
            font.pixelSize: 112
            font.bold: true
        }

        transform: Rotation {
            id: upperHinge

            origin.x: upperHalf.width / 2
            origin.y: upperHalf.height
            axis.x: 1
            axis.y: 0
            axis.z: 0
            angle: 0
        }
    }

    // Animated lower half showing the next character.
    Item {
        id: lowerFlap

        x: 0
        y: flipTile.height / 2
        z: 2
        width: flipTile.width
        height: flipTile.height / 2
        clip: true

        Rectangle {
            anchors.fill: parent
            color: flipTile.color
            radius: flipTile.radius
        }

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

        transform: Rotation {
            id: lowerHinge

            origin.x: lowerFlap.width / 2
            origin.y: 0
            axis.x: 1
            axis.y: 0
            axis.z: 0
            angle: 90
        }
    }

    // Static lower half showing the current character.
    Item {
        id: lowerHalf

        x: 0
        y: flipTile.height / 2
        width: flipTile.width
        height: flipTile.height / 2
        clip: true

        Text {
            x: 0
            y: -parent.height
            width: flipTile.width
            height: flipTile.height
            text: flipTile.displayedCharacter
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            color: "white"
            font.pixelSize: 112
            font.bold: true
        }
    }

    // Center seam.
    Rectangle {
        x: 0
        y: flipTile.height / 2 - height / 2
        z: 3
        width: flipTile.width
        height: 2
        color: "#080808"
    }

    // Fold the upper half away, then unfold the lower half.
    SequentialAnimation {
        id: foldTest

        PropertyAction {
            target: upperHinge
            property: "angle"
            value: 0
        }

        PropertyAction {
            target: lowerHinge
            property: "angle"
            value: 90
        }

        NumberAnimation {
            target: upperHinge
            property: "angle"
            from: 0
            to: -90
            duration: 400
        }

        NumberAnimation {
            target: lowerHinge
            property: "angle"
            from: 90
            to: 0
            duration: 400
        }

        onFinished: {
            flipTile.displayedCharacter = flipTile.character
            upperHinge.angle = 0
            lowerHinge.angle = 90
        }
    }

    TapHandler {
        onTapped: {
            if (flipTile.character !== flipTile.displayedCharacter && !foldTest.running) {
                foldTest.start()
            }
        }

    }
}
