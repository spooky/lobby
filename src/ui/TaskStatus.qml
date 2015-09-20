import QtQuick 2.3
import QtQuick.Controls 1.2
import QtQuick.Controls.Styles 1.2
import QtQuick.Layouts 1.1

RowLayout {
    id: item

    property string text
    property bool indefinite: false
    property bool running: false
    property real progress: 0.0

    property int h: 14

    spacing: 5

    BusyIndicator {
        visible: item.running && item.indefinite
        running: item.running
        implicitHeight: item.h
        implicitWidth: implicitHeight
    }

    ProgressBar {
        visible: item.running && !item.indefinite
        height: item.h / 2
        anchors.verticalCenter: parent.verticalCenter
        value: item.progress
        style: ProgressBarStyle {
            background: Rectangle {
                color: "transparent"
                border.color: root.textColor
                border.width: 1
                implicitWidth: 96
                implicitHeight: item.h / 2
            }
            progress: Rectangle {
                color: root.textColor
                border.color: root.textColor
            }
        }
    }

    Label {
        text: item.text
        color: root.textColor
        visible: item.running
    }
}
