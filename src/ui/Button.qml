import QtQuick 2.3
import QtQuick.Controls 1.2 as Controls
import QtQuick.Controls.Styles 1.2

Controls.Button {
    property string text
    property real textPointSize: 8
    property color textColor: root.backgroundColor
    property color backgroundColor: root.textHighlightColor
    property color pressedBackgroundColor: root.textColor
    property color borderColor: root.textHighlightColor
    property int implicitWidth: 64
    property int implicitHeight: 24

    style: ButtonStyle {
        label: Text {
            renderType: Text.NativeRendering
            text: control.text
            font.pointSize: textPointSize
            color: textColor
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
        }
        background: Rectangle {
            implicitWidth: control.implicitWidth
            implicitHeight: control.implicitHeight
            border.width: control.activeFocus ? 2 : 1
            border.color: control.activeFocus & !control.pressed ? pressedBackgroundColor : borderColor
            color: control.pressed ? pressedBackgroundColor : backgroundColor
        }
    }
}
