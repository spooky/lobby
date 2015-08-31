import QtQuick 2.3
import QtQuick.Controls 1.2
import QtQuick.Window 2.2
import QtQuick.Layouts 1.0

GroupBox {
    title: qsTr("Featured mods")
    flat: true

    ListModel {
        id: featuredMods

        ListElement { name: "FAF" }
        ListElement { name: "Phantom-X" }
        ListElement { name: "Nomads" }
    }

    Column {
        anchors.left: parent.left
        anchors.right: parent.right

        GridLayout {
            columns: 2
            anchors.left: parent.left
            anchors.right: parent.right

            TextField {
                placeholderText: qsTr("featured mod")
                Layout.column: 0
                Layout.fillWidth: true
            }

            Button {
                text: qsTr("Add")
                Layout.column: 1
            }
        }

        Repeater {
            model: featuredMods
            delegate: Text {
                text: name
            }
        }
    }
}