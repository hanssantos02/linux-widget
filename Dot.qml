import QtQuick

Rectangle {
    property bool lit: true
    width: 14
    height: width
    radius: width / 2
    color: lit ? "white" : "#303030"
}
