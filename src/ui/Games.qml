import QtQuick 2.2

Flow {
    anchors.fill: parent
    anchors.margins: 5
    spacing: 5

    NewGame {
        onClicked: contentModel.hostGame()
    }

    GameTile {
        title: "join here if you dare"
        host: "me"
        players: 1
        slots: 4
        balance: 25
    }

    // Repeater {
    //     model: contentModel.games

    //     delegate: GameTile {
    //         title: "one"
    //         host: "me"
    //         players: 1
    //         slots: 4
    //         balance: 11
    //     }
    // }
}