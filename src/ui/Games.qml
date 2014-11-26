import QtQuick 2.2

Flow {
    anchors.fill: parent
    anchors.margins: 5
    spacing: 5

    NewGame {
        onClicked: contentModel.hostGame()
    }

    GameTile {}
    GameTile {}
    GameTile {}
    GameTile {}
    GameTile {}
}