import QtQuick 2.3
import QtQuick.Controls 1.2 as Controls
import QtQuick.Controls.Styles 1.2

Controls.CheckBox {
    id: ctrl

    property string text
    property color textColor: root.textColor

    style: CheckBoxStyle {
        label: Text {
            color: textColor
            text: ctrl.text
        }
    }
}