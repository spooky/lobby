import QtQuick 2.0

Rectangle {
    property string map: "icons/_temp_map.png" // "icons/unknown_map.svg"
    property string title: "Game title that is 25 chr"
    property string host: "spooky"
    property int players: 8
    property int slots: 12
    property int balance: 66

    // TODO: mods

    property int padding: 5
    property string textColor: root.textColor
    property string headingColor: root.textHighlightColor
    property string balanceColor: root.cybRed
    property string highlightColor: root.highlightColor

    signal clicked

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
                text: title
                color: headingColor
                wrapMode: Text.Wrap
                font.pixelSize: 14
                anchors.top: parent.top
                anchors.left: parent.left
                anchors.right: parent.right
            }

            Text {
                text: qsTr("by %1").arg(host)
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
                    text: qsTr("%1/%2").arg(players).arg(slots)
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
                    text: balance + "%"
                    color: balanceColor // TODO
                    font.pixelSize: 12
                }
            }
        }

        MouseArea {
            id: mouseArea
            anchors.fill: parent
            hoverEnabled: true
            onDoubleClicked: wrapper.clicked()
        }
    }
}
