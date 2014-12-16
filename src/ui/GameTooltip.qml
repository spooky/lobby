import QtQuick 2.0
import QtQuick.Layouts 1.1

Rectangle {
    // data
    property string map
    property string gameTitle
    property string gameHost
    property string mapName
    property string featuredModName
    property variant modNames: []
    property int slotsTaken
    property int slotsTotal
    property int gameBalance
    property variant teams: []

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

    function getFlag(cc) {
        // TODO
        return "../../res/chat/countries/" + cc.toLowerCase() + ".png";
    }
 
    Column {
        id: contentColumn
        anchors.margins: gutter
        spacing: padding
        x: gutter
        y: gutter

        Row {
            id: gameMeta
            spacing: padding

            Image {
                fillMode: Image.PreserveAspectCrop
                source: map || "icons/unknown_map.svg"
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
                    Text { text: qsTr("with"); font.pixelSize: textSize; color: textColor; visible: modNames.length > 0 }
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
                model: teams

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
                                    source: getFlag(modelData.cc)
                                    sourceSize: Qt.size(playerName.height, playerName.height)
                                    smooth: true
                                    anchors.verticalCenter: parent.verticalCenter
                                }
                                Text {
                                    id: playerName
                                    text: modelData.name
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
