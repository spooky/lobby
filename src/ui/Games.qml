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
            gameTitle: title
            gameHost: host
            slotsTaken: players
            slotsTotal: slots
            gameBalance: balance

            onDoubleClicked: contentModel.joinGame(id)
        }
    }
}