import QtQuick 2.3

Rectangle {
    id: wrapper
    anchors.verticalCenter: parent.verticalCenter
    anchors.rightMargin: 5
    width: childrenRect.width
    state: "closed"
    states: [
        State {
            name: "open"
            PropertyChanges { target: wrapper; color: mouseArea.containsMouse ? hover : background }
        },
        State {
            name: "closed"
            PropertyChanges { target: wrapper; color: mouseArea.containsMouse ? hover : "transparent" }
        }
    ]

    property string background
    property string hover
    signal clicked

    Row {
        spacing: 5
        x: 5

        Text {
            text: loginModel.loggedin ? loginModel.user : "log in"
            anchors.verticalCenter: parent.verticalCenter
            color: "#969696"
        }

        Item {
            width: 30
            height: 30
            anchors.verticalCenter: parent.verticalCenter

            Image {
                source: "icons/user.svg"
                sourceSize: Qt.size(24, 24)
                anchors.centerIn: parent
            }
        }
    }

    MouseArea {
        id: mouseArea
        hoverEnabled: true
        anchors.fill: parent
        cursorShape: Qt.PointingHandCursor
        onClicked: wrapper.clicked()
    }
}
