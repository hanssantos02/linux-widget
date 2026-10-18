import QtQuick

Grid {
    id: digitGrid

    width: columns * dotSize + (columns - 1) * spacing
    height: 7 * dotSize + 6 * spacing
    columns: 5
    spacing: 4

    required property string pattern

    Repeater {
        model: 35

        delegate: Dot {
            required property int index

            lit: digitGrid.pattern[index] === "1"

            width: digitGrid.dotSize
        }
    }

    property int dotSize: 14
}
