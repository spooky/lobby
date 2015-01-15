import QtQuick 2.3

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
            ComboBox {
                anchors.left: parent.left
                anchors.right: parent.right
                editable: true
            }
            TextField {
                anchors.left: parent.left
                anchors.right: parent.right
                placeholderText: qsTr("game title")
            }
            ComboBox {
                anchors.left: parent.left
                anchors.right: parent.right
                editable: true
            }
            ComboBox {
                anchors.left: parent.left
                anchors.right: parent.right
                editable: true
            }

            CheckBox {
                text: "mod 1"
            }
            CheckBox {
                text: "mod 2"
            }
            CheckBox {
                text: "mod 3"
            }
        }
    }
}