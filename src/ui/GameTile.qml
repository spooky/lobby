import QtQuick 2.0

Rectangle {
    property string map: "icons/unknown_map.svg"
    property string gameTitle
    property string gameHost
    property int slotsTaken
    property int slotsTotal
    property int gameBalance

    // TODO: mods

    property int padding: 5
    property string textColor: root.textColor
    property string headingColor: root.textHighlightColor
    property string balanceColor: root.cybRed
    property string highlightColor: root.highlightColor

    signal doubleClicked

    id: wrapper
    width: 200 + 2*padding
    height: 100 + 2*padding
    color: mouseArea.containsMouse ? highlightColor : "transparent"

    Item {
        anchors.fill: parent
        anchors.margins: padding

        Image {
            id: mapThumb
            fillMode: Image.PreserveAspectCrop
            source: map
            sourceSize: Qt.size(parent.height, parent.height)
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            smooth: true
        }

        Item {
            anchors.top: parent.top
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.left: mapThumb.right
            anchors.leftMargin: padding

            Text {
                id: titleText
                text: gameTitle
                color: headingColor
                wrapMode: Text.Wrap
                font.pixelSize: 14
                anchors.top: parent.top
                anchors.left: parent.left
                anchors.right: parent.right
            }

            Text {
                text: qsTr("by %1").arg(gameHost)
                font.pixelSize: 10
                color: textColor
                anchors.topMargin: padding
                anchors.top: titleText.bottom
                anchors.right: parent.right
                anchors.left: parent.left
            }

            Row {
                id: mods
                anchors.bottomMargin: padding
                anchors.bottom: playerConfig.top
                anchors.left: parent.left
                anchors.right: parent.right
                spacing: padding

                Image {
                    fillMode: Image.PreserveAspectCrop
                    source: "icons/faf.png"
                    sourceSize: Qt.size(16, 16)
                    smooth: true
                }

                Rectangle {
                    color: "transparent"
                    border.color: textColor
                    width: 16
                    height: 16

                    Text {
                        anchors.centerIn: parent
                        text: qsTr("10")
                        color: textColor
                    }
                }
            }

            Row {
                id: playerConfig
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                anchors.right: parent.right
                spacing: padding

                Text {
                    text: qsTr("%1/%2").arg(slotsTaken).arg(slotsTotal)
                    color: textColor
                    font.pixelSize: 12
                }
                Text {
                    text: qsTr("@")
                    anchors.verticalCenter: parent.verticalCenter
                    color: textColor
                    font.pixelSize: 10
                }
                Text {
                    text: gameBalance + "%"
                    color: balanceColor // TODO
                    font.pixelSize: 12
                }
            }
        }

        MouseArea {
            id: mouseArea
            anchors.fill: parent
            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor
            onDoubleClicked: wrapper.doubleClicked()
        }
    }
}
