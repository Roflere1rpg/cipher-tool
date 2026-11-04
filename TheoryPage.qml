import QtQuick
import QtQuick.Controls

// Общее оформление справки. Текст задаётся отдельно у каждого шифра.
ScrollView {
    property alias text: theory.text
    contentWidth: availableWidth

    TextArea {
        id: theory
        readOnly: true
        selectByMouse: true
        wrapMode: TextEdit.Wrap
        textFormat: TextEdit.PlainText
        font.pixelSize: 16
    }
}
