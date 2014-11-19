import QtQuick 2.2

Rectangle {
    property string textColor
    property string altColor
    property string highlightColor
    property int padding: 30

    signal clicked

    id: wrapper
    width: 200
    height: 100
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
        horizontalTileMode: BorderImage.Stretch
        verticalTileMode: BorderImage.Stretch
        smooth: true
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true
        onDoubleClicked: wrapper.clicked()
    }
}
