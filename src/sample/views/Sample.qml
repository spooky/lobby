import QtQuick 2.3
import QtQuick.Controls 1.2

import "../../ui" as Faf

Item {
    property int spacing: 5

    id: flow
    // the 'spacing fun' is here to provide content padding
    width: centralWidget.viewport.width - 2*spacing
    height: childrenRect.height + 2*spacing
    x: spacing
    y: spacing

    Text {
        text: 'Sample screen'
        horizontalAlignment: Text.AlignHCenter
        font.pixelSize: 16
        color: root.textColor
        anchors.centerIn: parent
    }
}
