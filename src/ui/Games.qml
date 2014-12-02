import QtQuick 2.2

Flow {
    anchors.fill: parent
    anchors.margins: 5
    spacing: 5

    NewGame {
        onDoubleClicked: contentModel.hostGame()
    }

    Repeater {
        model: contentModel.games

        GameTile {
            title: modelData.title
            host: modelData.host
            players: modelData.players
            slots: modelData.slots
            balance: modelData.balance

            onDoubleClicked: contentModel.joinGame(modelData.id)
        }
    }
}