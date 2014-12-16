import QtQuick 2.0

Rectangle {
    property string map
    property string gameTitle
    property string gameHost
    property int slotsTaken
    property int slotsTotal
    property int gameBalance

    // TODO: mods

    property var container
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

    function getX(pos, itemSize, tooltipSize, available, spacing) {
        if (pos + itemSize + 2*spacing + tooltipSize <= available)
            return pos + itemSize + 2*spacing;
        else if (pos - tooltipSize >= 0)
            return pos - tooltipSize;
        else
            return spacing;
    }

    function getY(pos, itemSize, tooltipSize, available, spacing) {
        if (pos + tooltipSize > available)
            return pos + itemSize - tooltipSize + spacing;
        else
            return pos + spacing;
    }

    GameTooltip {
        parent: container // HACK to force qml z indexing for tooltips to work as expected 
        x: getX(wrapper.x, wrapper.width, width, container.width, padding)
        y: getY(wrapper.y, wrapper.height, height, container.height, padding)
        z: 100
        visible: mouseArea.containsMouse ? true : false

        map: wrapper.map
        gameTitle: wrapper.gameTitle
        gameHost: wrapper.gameHost
        mapName: "TODO"
        featuredModName: "TODO"
        modNames: ["TODO", "TODO", "TODODO"]
        slotsTaken: wrapper.slotsTaken
        slotsTotal: wrapper.slotsTotal
        gameBalance: wrapper.gameBalance
        teams: [["cruchy (1100)"], ["creamy (0)"]]
        // teams: [["cruchy (1100)", "cookie (-200)"], ["candy (0)", "cupcake (2600)"]]
        // teams: [["cruchy (1100)", "cookie (-200)"], ["candy (0)", "cupcake (2600)"], ["creamy (0)"]]
    }

    Item {
        anchors.fill: parent
        anchors.margins: padding

        Image {
            id: mapThumb
            fillMode: Image.PreserveAspectCrop
            source: map || "icons/unknown_map.svg"
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
