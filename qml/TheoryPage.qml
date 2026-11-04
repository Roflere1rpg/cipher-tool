import QtQuick
import QtQuick.Controls

// Общее оформление справки. Текст задаётся отдельно у каждого шифра.
ScrollView {
    id: page
    property alias text: theory.text
    property bool markdown: false
    contentWidth: availableWidth

    TextArea {
        id: theory
        readOnly: true
        selectByMouse: true
        wrapMode: TextEdit.Wrap
        textFormat: page.markdown ? TextEdit.MarkdownText : TextEdit.PlainText
        font.pixelSize: 16
    }
}
