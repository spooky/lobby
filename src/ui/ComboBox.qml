import QtQuick 2.3
import QtQuick.Controls 1.2 as Controls
import QtQuick.Controls.Styles 1.2

Controls.ComboBox {
    property color textColor: root.textHighlightColor
    property color backgroundColor: root.altHighlightColor
    property color borderColor: root.textColor
    property color selectionColor: root.textHighlightColor
    property color selectedTextColor: root.backgroundColor
    property int implicitWidth: 100
    property int implicitHeight: 24

    model: ["lorem", "ipsum", "dolor"]

    style: ComboBoxStyle {
        dropDownButtonWidth: 17

        background: Rectangle {
            color: backgroundColor
            implicitWidth: control.implicitWidth
            implicitHeight: control.implicitHeight
            border.color: borderColor
            border.width: 1
        }
        label: Text {
            color: "red"
        }
    }
}