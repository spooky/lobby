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
            gameTitle: title
            gameHost: host
            mapPreviewSmall: map_preview_small
            mapPreviewBig: map_preview_big
            mapName: map_name
            featuredModName: featured_mod
            modNames: mods
            slotsTaken: player_count
            slotsTotal: slots
            teams: teams_arrangement
            gameBalance: balance
            container: flow.parent

            onDoubleClicked: contentModel.joinGame(id)
        }
    }
}
