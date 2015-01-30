import QtQuick 2.3
import QtQuick.Controls 1.2 as Controls
import QtQuick.Controls.Styles 1.2

Controls.CheckBox {
    property string text
    property color textColor: root.textColor
    property color borderColor: root.textColor
    property color activeBorderColor: root.textHighlightColor
    property int implicitWidth: 14
    property int implicitHeight: 14

    style: CheckBoxStyle {
        label: Text {
            color: textColor
            text: control.text
        }
        indicator: Rectangle {
            color: "transparent"
            implicitWidth: control.implicitWidth
            implicitHeight: control.implicitHeight
            border.color: control.activeFocus || control.hovered ? activeBorderColor : borderColor
            border.width: 1

            Image {
                visible: control.checked
                anchors.fill: parent
                anchors.margins: 1
                smooth: true
                source: "icons/tick.svg"
                fillMode: Image.PreserveAspectFit
                // sourceSize: Qt.size(control.width-2, control.height-2)
            }
        }
    }
}