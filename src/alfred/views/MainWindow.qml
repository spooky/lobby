import QtQuick 2.3
import QtQuick.Controls 1.2
import QtQuick.Window 2.2
import Qt.labs.settings 1.0


Window {
    id: alfred
    title: qsTr("Morning sir")
    width: 340
    height: 680
    visible: true
    flags: Qt.Tool

    Button {
        text: qsTr("Hello World")
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
    }
}