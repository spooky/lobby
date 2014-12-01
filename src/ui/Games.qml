import QtQuick 2.2

Flow {
    anchors.fill: parent
    anchors.margins: 5
    spacing: 5

    NewGame {
        onClicked: contentModel.hostGame()
    }

    Repeater {
        model: 2

        delegate: GameTile {
            title: "join here if you dare"
            host: "me"
            players: 1
            slots: 4
            balance: 66
        }
    }
}