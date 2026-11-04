import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

CipherPage {
    practiceComponent: Component {
        ColumnLayout {
            id: xorPractice
            spacing: 10

            property string resultText: ""
            property string stepsText: "Здесь появится результат."

            function resetResult() {
                resultText = ""
                stepsText = "Здесь появится результат."
            }

            function process(decrypt) {
                const answer = backend.process_xor(input.text, key.text, decrypt)
                resultText = answer.text
                stepsText = answer.steps
            }

            Label {
                text: "Шифр XOR"
                font.pixelSize: 26
                font.bold: true
            }
            Label {
                Layout.fillWidth: true
                text: "Побитовое исключающее ИЛИ (XOR). Ключ применяется к каждому символу."
                wrapMode: Text.WordWrap
            }

            RowLayout {
                spacing: 12
                Label { text: "Ключ" }
                TextField {
                    id: key
                    objectName: "keyField"
                    placeholderText: "Например: secret"
                    selectByMouse: true
                    onTextChanged: xorPractice.resetResult()
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
                    onTextChanged: xorPractice.resetResult()
                }
            }

            RowLayout {
                Button {
                    text: "Зашифровать"
                    enabled: input.text.length > 0 && key.text.length > 0
                    onClicked: xorPractice.process(false)
                }
                Button {
                    text: "Расшифровать"
                    enabled: input.text.length > 0 && key.text.length > 0
                    onClicked: xorPractice.process(true)
                }
                Button {
                    text: "Пример"
                    onClicked: {
                        key.text = "secret"
                        input.text = "Hello, world!"
                        xorPractice.process(false)
                    }
                }
                Button {
                    text: "Очистить"
                    onClicked: {
                        input.clear()
                        key.clear()
                        xorPractice.resetResult()
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
                    text: xorPractice.resultText
                    readOnly: true
                    selectByMouse: true
                    wrapMode: TextEdit.Wrap
                    textFormat: TextEdit.PlainText
                }
            }

            Label { text: "Пояснение" }
            ScrollView {
                Layout.fillWidth: true
                Layout.preferredHeight: 130
                contentWidth: availableWidth
                TextArea {
                    text: xorPractice.stepsText
                    readOnly: true
                    selectByMouse: true
                    wrapMode: TextEdit.Wrap
                    textFormat: TextEdit.PlainText
                }
            }
        }
    }
    theoryText: "ШИФР XOR\n\n"
        + "Побитовое исключающее ИЛИ. Работает с двоичным кодом символов.\n\n"
        + "1. Каждый символ текста и ключа превращается в число (код).\n"
        + "2. Числа переводятся в двоичную систему.\n"
        + "3. Применяется операция XOR: если биты разные — 1, если одинаковые — 0.\n"
        + "4. Результат переводится обратно в символ.\n\n"
        + "Свойство: A XOR K XOR K = A. Поэтому расшифровка — это повторное применение того же ключа.\n\n"
        + "Пример: 'A' (65) XOR 3 = 66 ('B'). 66 XOR 3 = 65 ('A')."
}
