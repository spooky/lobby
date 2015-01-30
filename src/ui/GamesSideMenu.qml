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

        Column {
            anchors.margins: 10
            anchors.fill: parent
            spacing: 5

            Button {
                anchors.right: parent.right
                text: qsTr("Host")
            }
            RowLayout {
                spacing: parent.spacing
                anchors.left: parent.left
                anchors.right: parent.right

                ComboBox {
                    editable: false
                    Layout.fillWidth: true
                }
                ActionIcon {
                    anchors.verticalCenter: parent.verticalCenter
                    implicitWidth: 18
                    size: 26
                    source: "icons/save.svg"
                    transform: Translate { x: 1 } // align to the right edge
                    onClicked: {
                        console.log('TODO: save preset action')
                    }
                }
            }
            RowLayout {
                spacing: parent.spacing
                anchors.left: parent.left
                anchors.right: parent.right

                TextField {
                    placeholderText: qsTr("game title")
                    Layout.fillWidth: true
                }
                LockButton {
                    anchors.verticalCenter: parent.verticalCenter
                    implicitWidth: 18
                    transform: Translate { x: 4 } // align to the right edge
                }
            }
            ComboBox {
                anchors.left: parent.left
                anchors.right: parent.right
                editable: true
            }
            ComboBox {
                anchors.left: parent.left
                anchors.right: parent.right
                editable: false
            }

            CheckBox {
                text: "mod 1"
                checked: true
            }
            CheckBox {
                text: "mod 2"
                checked: true
            }
            CheckBox {
                text: "mod 3"
            }
        }
    }
}