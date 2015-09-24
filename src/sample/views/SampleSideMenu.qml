import QtQuick 2.3
import QtQuick.Layouts 1.1

import "../../views" as Faf


Item {
    anchors.horizontalCenter: parent.horizontalCenter
    anchors.top: parent.top
    anchors.bottom: parent.bottom

    Column {
        id: icons
        spacing: 10

        Faf.ActionIcon {
            source: "../sample/views/icon.svg"
            anchors.horizontalCenter: parent.horizontalCenter

            onClicked: contentModel.doingThings()
        }
    }
}