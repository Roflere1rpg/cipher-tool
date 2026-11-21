import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ColumnLayout {
    id: matrix
    property string title: ""
    property var cells: []
    property var comparison: []
    property bool highlightChanges: false
    spacing: 6

    Label { text: matrix.title; font.bold: true }
    GridLayout {
        Layout.fillWidth: true
        columns: 4
        columnSpacing: 4
        rowSpacing: 4
        Repeater {
            model: 16
            delegate: Rectangle {
                required property int index
                Layout.fillWidth: true
                Layout.preferredHeight: 36
                radius: 4
                property bool changed: matrix.highlightChanges
                    && matrix.cells.length === 16 && matrix.comparison.length === 16
                    && matrix.cells[index] !== matrix.comparison[index]
                color: changed ? "#d2eee5" : "#eef1f4"
                border.color: changed ? "#488675" : "#cbd2da"
                Label {
                    anchors.centerIn: parent
                    text: matrix.cells.length === 16 ? matrix.cells[index] : "—"
                    font.family: "Consolas"
                    font.pixelSize: 18
                    color: "#172d38"
                }
            }
        }
    }
}
