import QtQuick 2.2
import QtGraphicalEffects 1.0


Item {
    property string source: "icons/rss.svg"
    property int size: 42
    property int glowRadius: 3
    property string glowColor: "#f1c240" // uef: 2d78b2, cyb: df2d0e, aeon: 0a9d2f, sera: f1c240
    property string overlayColor: "#f0f0f0"
    property real fadeSpeed: 140

    signal clicked

    id: wrapper // to provide padding so that the glow is not trimmed to the icon size
    width: size
    height: size

    Image {
        id: icon
        anchors.centerIn: parent
        source: wrapper.source
        sourceSize: Qt.size(wrapper.size - 2*glowRadius, wrapper.size - 2*glowRadius)
        smooth: true
        z: 20
    }

    // need opengl lib for this to work...
    // Glow {
    //     cached: true
    //     anchors.fill: wrapper
    //     radius: wrapper.glowRadius
    //     samples: 32
    //     color: wrapper.glowColor
    //     source: wrapper
    //     z: 10
    //     opacity: mouseArea.containsMouse ? 1 : 0

    //     Behavior on opacity { NumberAnimation { duration: wrapper.fadeSpeed; } }
    // }

    ColorOverlay {
        cached: true
        anchors.fill: icon
        color: wrapper.overlayColor
        source: icon
        z: 30
        opacity: mouseArea.containsMouse ? 0.9 : 0

        Behavior on opacity { NumberAnimation { duration: wrapper.fadeSpeed } }
    }

    MouseArea {
        id: mouseArea
        anchors.fill: icon
        hoverEnabled: true
        onClicked: wrapper.clicked()
    }
}
