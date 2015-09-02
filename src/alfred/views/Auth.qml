import QtQuick 2.3
import QtQuick.Controls 1.2
import QtQuick.Controls.Styles 1.4
import QtQuick.Window 2.2
import QtQuick.Layouts 1.0

Rectangle {
    color: auth.pending ? actionPendingColor : "transparent"
    height: childrenRect.height

    GroupBox {
        title: qsTr("Auth")
        flat: true
        anchors.left: parent.left
        anchors.right: parent.right

        GridLayout {
            columns: 3
            anchors.left: parent.left
            anchors.right: parent.right

            Text {
                text: auth.user || 'none'
                Layout.column: 0
                Layout.fillWidth: true
            }

            Button {
                text: qsTr("Accept")
                Layout.column: 1
                onClicked: auth.accept()
            }

            Button {
                text: qsTr("Reject")
                Layout.column: 2
                onClicked: auth.reject()
            }
        }
    }
}
