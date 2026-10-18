import QtQuick

Grid {
    id: digitGrid

    width: 86
    height: 122
    columns: 5
    spacing: 4

    required property string pattern

    Repeater {
        model: 35

        delegate: Dot {
            required property int index

            lit: digitGrid.pattern[index] === "1"
        }
    }
}
