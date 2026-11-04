import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ColumnLayout {
    id: page
    objectName: "caesarPractice"
    spacing: 10

    property string resultText: ""
    property string stepsText: "Здесь появятся первые 12 замен букв."

    function resetResult() {
        resultText = ""
        stepsText = "Здесь появятся первые 12 замен букв."
    }

    function process(decrypt) {
        const answer = backend.process_caesar(input.text, shift.value,
                                       language.currentText, decrypt)
        resultText = answer.text
        stepsText = answer.steps
    }

    Label {
        text: "Шифр Цезаря"
        font.pixelSize: 26
        font.bold: true
    }
    Label {
        Layout.fillWidth: true
        text: "Каждая буква сдвигается на заданное число позиций в алфавите."
        wrapMode: Text.WordWrap
    }

    RowLayout {
        spacing: 12
        Label { text: "Алфавит" }
        ComboBox {
            id: language
            model: ["Русский", "Английский"]
            onCurrentIndexChanged: page.resetResult()
        }
        Label { text: "Сдвиг" }
        SpinBox {
            id: shift
            from: 0
            to: language.currentIndex === 0 ? 32 : 25
            value: 3
            onValueChanged: page.resetResult()
        }
    }

    Label { text: "Исходный текст" }
    ScrollView {
        Layout.fillWidth: true
        Layout.fillHeight: true
        Layout.minimumHeight: 80
        contentWidth: availableWidth
        TextArea {
            id: input
            objectName: "inputText"
            placeholderText: "Например: Привет, мир!"
            wrapMode: TextEdit.Wrap
            textFormat: TextEdit.PlainText
            selectByMouse: true
            onTextChanged: page.resetResult()
        }
    }

    RowLayout {
        Button {
            text: "Зашифровать"
            enabled: input.text.length > 0
            onClicked: page.process(false)
        }
        Button {
            text: "Расшифровать"
            enabled: input.text.length > 0
            onClicked: page.process(true)
        }
        Button {
            text: "Пример"
            onClicked: {
                shift.value = 3
                input.text = language.currentIndex === 0 ? "Привет, мир!" : "Hello, world!"
                page.process(false)
            }
        }
        Button {
            text: "Очистить"
            onClicked: {
                input.clear()
                page.resetResult()
            }
        }
    }

    Label { text: "Результат (можно выделить и скопировать)" }
    ScrollView {
        Layout.fillWidth: true
        Layout.fillHeight: true
        Layout.minimumHeight: 80
        contentWidth: availableWidth
        TextArea {
            objectName: "resultText"
            text: page.resultText
            readOnly: true
            selectByMouse: true
            wrapMode: TextEdit.Wrap
            textFormat: TextEdit.PlainText
        }
    }

    Label { text: "Замены по шагам · позиции считаются с нуля" }
    ScrollView {
        Layout.fillWidth: true
        Layout.preferredHeight: 130
        contentWidth: availableWidth
        TextArea {
            text: page.stepsText
            readOnly: true
            selectByMouse: true
            wrapMode: TextEdit.Wrap
            textFormat: TextEdit.PlainText
        }
    }
    Label {
        Layout.fillWidth: true
        text: "В русском алфавите есть Ё. Символы вне выбранного алфавита не меняются."
        wrapMode: Text.WordWrap
    }
}