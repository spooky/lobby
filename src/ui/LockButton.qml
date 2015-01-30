import QtQuick 2.3
import QtQuick.Controls 1.2 as Controls
import QtQuick.Controls.Styles 1.2
import QtGraphicalEffects 1.0

Controls.CheckBox {
    property string text
    property color textColor: root.textColor
    property color colorActive: root.textHighlightColor
    property int implicitWidth: 14
    property int implicitHeight: 14

    style: CheckBoxStyle {
        label: Text {
            color: textColor
            text: control.text
        }

        indicator: Item {
            implicitWidth: control.implicitWidth
            implicitHeight: control.implicitHeight

            Image {
                id: icon
                fillMode: Image.PreserveAspectFit
                source: control.checked ? "icons/locked.svg" : "icons/unlocked.svg"
                sourceSize: Qt.size(parent.width, parent.height)
                smooth: true
            }

            ColorOverlay {
                visible: control.activeFocus || control.hovered
                cached: true
                color: colorActive
                source: icon
                anchors.fill: icon
            }
        }
    }
}