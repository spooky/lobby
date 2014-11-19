import QtQuick 2.2
import QtQuick.Layouts 1.0
import QtQuick.Controls 1.2
import QtQuick.Controls.Styles 1.2


Rectangle {
    property string background
    property string textColor
    property int padding: 5

    id: wrapper
    color: background
    width: childrenRect.width + 2*padding
    height: childrenRect.height + 2*padding

    Column {
        spacing: padding
        x: padding
        y: padding
        width: 150

        Item {
            width: parent.width
            height: childrenRect.height

            ActionIcon {
                source: "icons/settings.svg"
                size: 24
                anchors.right: logout.left
            }

            ActionIcon {
                id: logout
                source: "icons/logout.svg"
                size: 24
                anchors.right: parent.right
                onClicked: loginModel.logout()
            }
        }
    }
}
