import QtQuick 2.3
import QtQuick.Layouts 1.1

import "../../views" as Faf

Item {
    anchors.horizontalCenter: parent.horizontalCenter
    anchors.top: parent.top
    anchors.bottom: parent.bottom

    Column {
        id: icons
        spacing: 10

        Faf.ActionIcon {
            source: "icons/host.svg"
            anchors.horizontalCenter: parent.horizontalCenter
            onClicked: {
                hostOptionsPanel.state = hostOptionsPanel.state == "open" ? "closed" : "open"
            }
        }
    }

    Rectangle {
        id: hostOptionsPanel
        objectName: "hostOptionsPanel"
        width: 300
        color: root.highlightColor
        anchors.left: icons.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        state: "closed"
        states: [
            State {
                name: "open"
                PropertyChanges { target: hostOptionsPanel; visible: sideMenu.state == "open" && true }
            },
            State {
                name: "closed"
                PropertyChanges { target: hostOptionsPanel; visible: false }
            }
        ]

        GridLayout {
            anchors.margins: 10
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.right: parent.right
            columns: 2

            Faf.Button {
                Layout.row: 1
                Layout.column: 1
                Layout.alignment: Qt.AlignVCenter | Qt.AlignRight

                text: qsTr("Host")
                onClicked: contentModel.hostGame()
            }

            Faf.ComboBox {
                Layout.row: 2
                Layout.column: 1
                Layout.fillWidth: true

                id: presets
                editable: true
                model: contentModel.presets
                textRole: 'name'
                currentIndex: model.currentIndex
                onActivated: model.setSelected(index)
            }

            Faf.ActionIcon {
                Layout.row: 2
                Layout.column: 2
                Layout.alignment: Qt.AlignVCenter | Qt.AlignRight

                implicitWidth: 18
                size: 26
                source: "icons/save.svg"
                transform: Translate { x: 1 } // align to the right edge
                onClicked: contentModel.savePreset(presets.editText)
            }

            Faf.TextField {
                Layout.row: 3
                Layout.column: 1
                Layout.fillWidth: true

                id: title
                placeholderText: qsTr("game title")
                text: contentModel.title
                onTextChanged: contentModel.title = text
            }

            Faf.LockButton {
                Layout.row: 3
                Layout.column: 2
                Layout.alignment: Qt.AlignVCenter | Qt.AlignRight

                id: locked
                checked: contentModel.private
                implicitWidth: 18
                transform: Translate { x: 4 } // align to the right edge
                onCheckedChanged: contentModel.private = checked
            }

            Faf.ComboBox {
                Layout.row: 4
                Layout.column: 1
                Layout.fillWidth: true

                id: featured
                editable: false
                model: contentModel.featured
                textRole: 'name'
                currentIndex: model.currentIndex
                onActivated: model.setSelected(index)
            }

            Faf.ComboBox {
                Layout.row: 5
                Layout.column: 1
                Layout.fillWidth: true

                id: mapCode
                editable: true
                model: contentModel.maps
                textRole: 'name'
                currentIndex: model.currentIndex
                onActivated: model.setSelected(index)
            }

            ColumnLayout {
                Layout.row: 6
                Layout.column: 1
                Layout.fillWidth: true

                Repeater {
                    id: mods
                    model: contentModel.mods

                    delegate: Faf.CheckBox {
                        checked: model.item.selected
                        text: model.item.name
                        onClicked: model.item.toggleSelected()
                    }
                }
            }
        }
    }
}