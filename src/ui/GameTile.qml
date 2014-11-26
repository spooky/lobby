import QtQuick 2.0

Rectangle {
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
            id: map
            fillMode: Image.PreserveAspectCrop
            source: "icons/_temp_map.png"
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
            anchors.left: map.right
            anchors.leftMargin: padding

            Text {
                id: title
                text: qsTr("Game title that is 25 chr")
                color: headingColor
                wrapMode: Text.Wrap
                font.pixelSize: 14
                anchors.top: parent.top
                anchors.left: parent.left
                anchors.right: parent.right
            }

            Text {
                id: host
                text: qsTr("by spooky")
                font.pixelSize: 10
                color: textColor
                anchors.topMargin: padding
                anchors.top: title.bottom
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
                    text: qsTr("10/12")
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
                    text: qsTr("21%")
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
