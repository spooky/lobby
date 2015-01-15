import QtQuick 2.3
import QtQuick.Controls 1.2 as Controls
import QtQuick.Controls.Styles 1.2

Controls.TextField {
    textColor: root.textHighlightColor

    property color backgroundColor: root.altHighlightColor
    property color borderColor: root.textColor
    property color selectionColor: root.textHighlightColor
    property color selectedTextColor: root.backgroundColor
    property color placeholderTextColor: root.paleTextColor
    property int implicitWidth: 100
    property int implicitHeight: 24

    style: TextFieldStyle {
        selectionColor: control.selectionColor
        selectedTextColor: control.selectedTextColor
        placeholderTextColor: control.placeholderTextColor

        background: Rectangle {
            color: backgroundColor
            implicitWidth: control.implicitWidth
            implicitHeight: control.implicitHeight
            border.color: borderColor
            border.width: 1
        }
    }
}
