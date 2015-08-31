import QtQuick 2.3
import QtQuick.Controls 1.2
import QtQuick.Window 2.2


Window {
    id: alfred
    title: qsTr("Morning sir")
    width: 340
    height: 680
    flags: Qt.Tool

    Column {
        anchors.fill: parent

        FeaturedMods {
            anchors.left: parent.left
            anchors.right: parent.right
        }
    }
}
