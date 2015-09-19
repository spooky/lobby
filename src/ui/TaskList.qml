import QtQuick 2.3
import QtQuick.Controls 1.2
import QtQuick.Layouts 1.1


Rectangle {
    property int itemPadding: 5
    property color itemColor: root.highlightColor

    color: backgroundColor
    width: childrenRect.width
    height: childrenRect.height

    ColumnLayout {
        spacing: 1
        anchors.top: parent.top

        Repeater {
            model: windowModel.taskList

            Rectangle {
                color: itemColor
                height: 24 // childrenRect.height + 2*itemPadding
                Layout.fillWidth: true
                Layout.minimumWidth: childrenRect.width + 2*itemPadding

                TaskItem {
                    anchors.top: parent.top
                    anchors.left: parent.left
                    anchors.margins: itemPadding

                    text: model.text
                    indefinite: model.indefinite
                    progress: model.progress
                    running: model.running
                }
            }
        }
    }
}
