import QtQuick 2.0
import QtQuick.Layouts 1.1

Rectangle {
    // data
    property string map: "icons/unknown_map.svg"
    property string gameTitle: "game title"
    property string gameHost: "host name"
    property string mapName: "map name"
    property string featuredModName: "featured mod"
    property variant modNames: ["lorem", "ipsum", "dolor", "sit", "amet"]
    property int slotsTaken: 4
    property int slotsTotal: 8
    property int gameBalance: 66

    // ui
    property int padding: 5
    property double gutter: padding*1.618
    property int thumbSize: 128
    property int headingTextSize: 16
    property int textSize: 13
    property string textColor: root.textColor
    property string headingColor: root.textHighlightColor
    property string balanceColor: root.seraGold
    property string highlightColor: root.highlightColor
    property string altHighlightColor: root.altHighlightColor

    id: wrapper
    color: highlightColor
    border.color: altHighlightColor
    width: childrenRect.width + 2*gutter
    height: childrenRect.height + 2*gutter

    Column {
        id: contentColumn
        anchors.margins: padding*1.618
        spacing: padding
        x: gutter
        y: gutter

        Row {
            id: gameMeta
            spacing: padding

            Image {
                fillMode: Image.PreserveAspectCrop
                source: map
                sourceSize: Qt.size(thumbSize, thumbSize)
                smooth: true
            }

            Column {
                Text { text: gameTitle; color: headingColor; font.pixelSize: headingTextSize }
                Text { text: qsTr("by %1").arg(gameHost); font.pixelSize: textSize; color: textColor }
                Text { text: qsTr("on %1").arg(mapName); font.pixelSize: textSize; color: textColor }
                Text { text: " "; font.pixelSize: textSize } // spacer

                Row {
                    spacing: padding

                    Text { text: qsTr("mod"); font.pixelSize: textSize; color: textColor }
                    Text { text: featuredModName; font.pixelSize: textSize; color: headingColor; font.weight: Font.DemiBold }
                    Text { text: qsTr("with"); font.pixelSize: textSize; color: textColor }
                }

                Repeater {
                    model: modNames
                    Text { text: "- " + modelData; font.pixelSize: textSize; color: textColor }
                }
            }
        }

        Text { text: qsTr("Teams (%1/%2)").arg(slotsTaken).arg(slotsTotal); color: headingColor; font.pixelSize: headingTextSize }

        Row {
            spacing: padding

            Repeater {
                id: playerSetup
                // model: [["cruchy (1100)"], ["candy (0)"]]
                model: [["cruchy (1100)", "cookie (-200)"], ["candy (0)", "cupcake (2600)"]]
                // model: [["cruchy (1100)", "cookie (-200)"], ["candy (0)", "cupcake (2600)"], ["creamy (0)"]]

                Row {
                    id: team
                    spacing: padding

                    property int first: index == 0
                    property int last: index == playerSetup.count-1

                    Column {
                        Repeater {
                            model: modelData

                            Row {
                                spacing: padding
                                // to stretch the teams at least to the tooptip width
                                width: Math.max(playerName.contentWidth + countryFlag.width + spacing, parent.width, (gameMeta.width - (playerSetup.count-1)*separator.width)/playerSetup.count)
                                layoutDirection: last ? Qt.RightToLeft : Qt.LeftToRight
                                anchors.horizontalCenter: parent.horizontalCenter

                                Image {
                                    id: countryFlag
                                    fillMode: Image.PreserveAspectCrop
                                    source: "../../res/chat/countries/pl.png"
                                    sourceSize: Qt.size(playerName.height, playerName.height)
                                    smooth: true
                                    anchors.verticalCenter: parent.verticalCenter
                                }
                                Text {
                                    id: playerName
                                    text: modelData
                                    color: textColor
                                    font.pixelSize: textSize
                                    horizontalAlignment: team.first ? Text.AlignLeft : team.last ? Text.AlignRight : Text.AlignHCenter
                                } 
                            }
                        }
                    }
                    Text {
                        id: separator
                        text: "vs"
                        color: headingColor
                        font.pixelSize: textSize
                        anchors.verticalCenter: parent.verticalCenter
                        visible: index != playerSetup.count-1
                    }
                }
            }
        }

        Row {
            spacing: padding
            anchors.horizontalCenter: parent.horizontalCenter
            Text { text: gameBalance + "%"; color: balanceColor; font.pixelSize: headingTextSize }
            Text { text: qsTr("balanced"); color: headingColor; font.pixelSize: headingTextSize }
        }
    }
}
