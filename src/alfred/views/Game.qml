import QtQuick 2.3
import QtQuick.Controls 1.2
import QtQuick.Controls.Styles 1.4
import QtQuick.Window 2.2
import QtQuick.Layouts 1.0

Rectangle {
    height: childrenRect.height

    GroupBox {
        title: qsTr("Game")
        flat: true
        anchors.left: parent.left
        anchors.right: parent.right

        GridLayout {
            columns: 3
            anchors.left: parent.left
            anchors.right: parent.right

            TextField {
                id: gameJson
                text: game.gameJson
                placeholderText: 'game json'
                Layout.column: 0
                Layout.fillWidth: true
            }

            Button {
                text: qsTr("Create")
                Layout.column: 1
                onClicked: game.create(gameJson.text)
            }

            Button {
                text: qsTr("Generate")
                Layout.column: 2
                onClicked: game.generate()
            }
        }
    }
}
