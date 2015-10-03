import QtQuick 2.3
import QtQuick.Controls 1.2
import QtQuick.Window 2.2
import Qt.labs.settings 1.0

Window {
    id: alfred
    title: qsTr("Morning sir")
    width: 340
    height: 680
    flags: Qt.Tool

    property color actionPendingColor: "#308594AE"

    // remember window geometry
    Settings {
        property alias a_x: alfred.x
        property alias a_y: alfred.y
        property alias a_width: alfred.width
        property alias a_height: alfred.height
    }

    Column {
        anchors.fill: parent

        // FeaturedMods {
        //     anchors.left: parent.left
        //     anchors.right: parent.right
        // }

        Auth {
            anchors.left: parent.left
            anchors.right: parent.right
        }

        Game {
            anchors.left: parent.left
            anchors.right: parent.right
        }
    }
}
