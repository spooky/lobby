import QtQuick 2.3

Flow {
    id: flow
    anchors.fill: parent
    anchors.margins: 5
    spacing: 5

    NewGame {
        onDoubleClicked: contentModel.hostGame()
    }

    Repeater {
        id: repeater
        model: contentModel.games

        GameTile {
            id: item
            gameTitle: title
            gameHost: host
            slotsTaken: players
            slotsTotal: slots
            gameBalance: balance
            container: flow.parent

            onDoubleClicked: contentModel.joinGame(id)
        }
    }
}