import QtQuick 2.3
import QtQuick.Layouts 1.1

Item {
    anchors.horizontalCenter: parent.horizontalCenter
    anchors.top: parent.top
    anchors.bottom: parent.bottom

    function storeOptions() {
        contentModel.title = title.text
        contentModel.private = locked.checked
        contentModel.featured = featured.currentText
        contentModel.map_code = map_code.currentText

        for (var i=0; i<mods.model.count; i++) {
            console.log(mods.model.get(i).selected)
        }

        contentModel.mods = mods.model
    }

    Column {
        id: icons
        spacing: 10

        ActionIcon {
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

            Button {
                Layout.row: 1
                Layout.column: 1
                Layout.alignment: Qt.AlignVCenter | Qt.AlignRight

                text: qsTr("Host")
                onClicked: {
                    storeOptions()
                    contentModel.hostGame()
                }
            }

            ComboBox {
                Layout.row: 2
                Layout.column: 1
                Layout.fillWidth: true

                editable: false
                model: ["default", "final rush", "training"]

            }

            ActionIcon {
                Layout.row: 2
                Layout.column: 2
                Layout.alignment: Qt.AlignVCenter | Qt.AlignRight

                implicitWidth: 18
                size: 26
                source: "icons/save.svg"
                transform: Translate { x: 1 } // align to the right edge
                onClicked: {
                    console.log('TODO: save preset action')
                }
            }

            TextField {
                Layout.row: 3
                Layout.column: 1
                Layout.fillWidth: true

                id: title
                placeholderText: qsTr("game title")
                text: contentModel.title
            }

            LockButton {
                Layout.row: 3
                Layout.column: 2
                Layout.alignment: Qt.AlignVCenter | Qt.AlignRight

                id: locked
                checked: contentModel.private
                implicitWidth: 18
                transform: Translate { x: 4 } // align to the right edge
            }

            ComboBox {
                Layout.row: 4
                Layout.column: 1
                Layout.fillWidth: true

                id: featured
                editable: false
                model: ["Forged Alliance Forever", "Phantom X", "Vanilla", "The Nomads"]
            }

            ComboBox {
                Layout.row: 5
                Layout.column: 1
                Layout.fillWidth: true

                id: map_code
                editable: true
                model: ["Seton's", "Sandbox", "Regor"]
            }

            ColumnLayout {
                Layout.row: 6
                Layout.column: 1
                Layout.fillWidth: true

                Repeater {
                    id: mods
                    model: ListModel {
                        ListElement {
                            name: "rks_explosions"
                            selected: true
                        }
                        ListElement {
                            name: "Final Rush Pro"
                            selected: false
                        }
                        ListElement {
                            name: "eco info"
                            selected: true
                        }
                    }

                    delegate: CheckBox {
                        id: checkbox
                        checked: selected
                        text: name
                        onClicked: mods.model.set(index, { "selected": checkbox.checked })
                    }
                }
            }
        }
    }
}