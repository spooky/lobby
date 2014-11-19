import QtQuick 2.2

Grid {
    anchors.fill: parent
    anchors.margins: 5
    spacing: 5

    NewGame {
        textColor: root.textColor
        altColor: root.altHighlightColor
        highlightColor: root.highlightColor
        onClicked: contentModel.hostGame()
    }
}