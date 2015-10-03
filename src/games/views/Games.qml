import QtQuick 2.3
import QtQuick.Controls 1.2


Flow {
    id: flow
    // the 'spacing fun' is here to provide content padding
    width: centralWidget.viewport.width - 2*spacing
    height: childrenRect.height + 2*spacing
    x: spacing
    y: spacing
    spacing: 5

    NewGame {
        onDoubleClicked: contentModel.hostGame()
    }

    Repeater {
        id: repeater
        model: contentModel.games

        GameTile {
            id: item
            gameTitle: model.title
            gameHost: model.host
            mapPreviewSmall: model.mapPreviewSmall
            mapPreviewBig: model.mapPreviewBig
            mapName: model.mapName
            featuredModName: model.featuredMod
            modNames: model.mods
            slotsTaken: model.players
            slotsTotal: model.slots
            teams: model.teams
            gameBalance: model.balance
            container: flow.parent

            onDoubleClicked: contentModel.joinGame(id)
        }
    }
}
