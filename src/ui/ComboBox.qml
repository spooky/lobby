import QtQuick 2.3
import QtQuick.Controls 1.2 as Controls
import QtQuick.Controls.Styles 1.2
import QtQuick.Controls.Private 1.0

Controls.ComboBox {
    property color textColor: root.textHighlightColor
    property color textColorDisabled: root.textColor
    property color backgroundColor: root.altHighlightColor
    property color backgroundColorDisabled: root.highlightColor
    property color editorBackgroundColor: root.paleTextColor
    property color selectedBackgroundColor: root.paleTextColor
    property color borderColor: root.textColor
    property color borderColorDisabled: root.paleTextColor
    property color borderColorActive: root.textHighlightColor
    property color selectionColor: root.textHighlightColor
    property color selectedTextColor: root.backgroundColor
    property int implicitWidth: 100
    property int implicitHeight: 24

    model: ["lorem", "ipsum", "dolor"]

    style: ComboBoxStyle {
        id: styleRoot
        dropDownButtonWidth: 17
        
        property color __borderColor: control.enabled ? (control.activeFocus ? borderColorActive : borderColor) : borderColorDisabled

        background: Rectangle {
            id: mainRect
            color: control.enabled ? backgroundColor : backgroundColorDisabled
            implicitWidth: control.implicitWidth
            implicitHeight: control.implicitHeight
            border.color: styleRoot.__borderColor
            border.width: 1

            Rectangle {
                id: glyph
                anchors.right: parent.right
                height: parent.height
                width: parent.height
                color: "transparent"
                states: State {
                    name: "inverted"
                    when: __popup.__popupVisible
                    PropertyChanges { target: glyph; rotation: 180 }
                }
                    
                Image {
                    id: glyphIcon
                    source: "icons/up.svg"
                    sourceSize: Qt.size(parent.height/2, parent.height/2)
                    smooth: true
                    anchors.centerIn: parent
                    transform: [
                        Rotation { origin.x: glyphIcon.width/2; origin.y: glyphIcon.height/2; angle: 180 },
                        Translate { y: 2 }
                    ]
                }
            }
        }

        label: Controls.Label {      
          verticalAlignment: Qt.AlignVCenter
          anchors.fill: parent
          text: control.currentText
          color: control.enabled ? textColor : textColorDisabled
        }

        __editor: Item {
            implicitWidth: 100
            implicitHeight: Math.max(25, Math.round(TextSingleton.implicitHeight * 1.2))
            clip: true

            Rectangle {
                anchors.bottomMargin: 1
                color: editorBackgroundColor
                anchors.fill: parent
                border.color: styleRoot.__borderColor
            }

            Rectangle {
                color: styleRoot.__borderColor
                anchors.bottomMargin: 2
                anchors.topMargin: 1
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                width: 1
            }
        }

        __dropDownStyle: MenuStyle {
            __maxPopupHeight: 600
            __menuItemType: "comboboxitem"
            __selectedBackgroundColor: selectedBackgroundColor
            __borderColor: styleRoot.__borderColor
            __scrollerStyle: ScrollViewStyle { }

            padding { top: 0; bottom: 0; left: 0; right: 0 }

            itemDelegate.background: Rectangle {
                visible: styleData.selected && styleData.enabled
                color: selectedBackgroundColor
            }
        }
    }
}