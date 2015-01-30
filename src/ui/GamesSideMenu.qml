import QtQuick 2.3
import QtQuick.Layouts 1.1

Item {
    anchors.horizontalCenter: parent.horizontalCenter
    anchors.top: parent.top
    anchors.bottom: parent.bottom

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

                placeholderText: qsTr("game title")
            }

            LockButton {
                Layout.row: 3
                Layout.column: 2
                Layout.alignment: Qt.AlignVCenter | Qt.AlignRight

                implicitWidth: 18
                transform: Translate { x: 4 } // align to the right edge
            }

            ComboBox {
                Layout.row: 4
                Layout.column: 1
                Layout.fillWidth: true

                editable: false
                model: ["Forged Alliance Forever", "Phantom X", "Vanilla", "The Nomads"]
            }

            ComboBox {
                Layout.row: 5
                Layout.column: 1
                Layout.fillWidth: true

                editable: true
                model: ["Seton's", "Sandbox", "Regor"]
            }

            ColumnLayout {
                Layout.row: 6
                Layout.column: 1
                Layout.fillWidth: true

                CheckBox {
                    text: "rks_explosions"
                    checked: true
                }
                CheckBox {
                    text: "Final Rush Pro"
                    checked: true
                }
                CheckBox {
                    text: "eco info"
                }
            }
        }
    }
}