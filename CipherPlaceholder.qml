import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

// Общее оформление для ещё не реализованных шифров.
// Каждая страница задаёт своё название и краткое описание.
ColumnLayout {
    id: placeholder
    property string cipherName: ""
    property string description: ""
    spacing: 12

    Label {
        text: placeholder.cipherName
        font.pixelSize: 26
        font.bold: true
    }
    Label {
        Layout.fillWidth: true
        text: placeholder.description
        wrapMode: Text.WordWrap
    }
    Label {
        Layout.fillWidth: true
        text: "Шифр пока не реализован. Здесь появятся ввод текста, параметры и результат."
        wrapMode: Text.WordWrap
    }

    // Пустой элемент занимает остаток высоты и прижимает текст к верху.
    Item { Layout.fillHeight: true }
}
