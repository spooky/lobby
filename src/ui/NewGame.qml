import QtQuick 2.2

Item {
    property string textColor: root.textColor
    property string altColor: root.altHighlightColor
    property string highlightColor: root.highlightColor
    property int padding: 30

    signal doubleClicked

    id: wrapper
    width: 210
    height: 110

    Rectangle {
        anchors.margins: 5
        anchors.fill: parent
        color: mouseArea.containsMouse ? highlightColor : "transparent"
        radius: height*0.15
        // border.color: altColor
        // border.width: 2

        Image {
            source: "icons/plus.svg"
            sourceSize: Qt.size(28, 28)
            smooth: true
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
            anchors.leftMargin: padding
        }

        Text {
            text: qsTr("Host Game")
            font.pointSize: 14
            color: textColor
            anchors.verticalCenter: parent.verticalCenter
            anchors.right: parent.right
            anchors.rightMargin: padding
        }

        BorderImage {
            source: "icons/dashborder.svg"
            width: parent.width
            height: parent.height
            anchors.centerIn: parent
            horizontalTileMode: BorderImage.Stretch
            verticalTileMode: BorderImage.Stretch
            smooth: true
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
