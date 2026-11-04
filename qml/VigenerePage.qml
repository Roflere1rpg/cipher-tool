import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

CipherPage {
    practiceComponent: Component {
        ColumnLayout {
            id: vigenerePractice
            spacing: 10

            property string resultText: ""
            property string stepsText: "Здесь появится результат."

            function resetResult() {
                resultText = ""
                stepsText = "Здесь появится результат."
            }

            function process(decrypt) {
                const answer = backend.process_vigenere(input.text, key.text,
                                                language.currentText, decrypt)
                resultText = answer.text
                stepsText = answer.steps
            }

            Label {
                text: "Шифр Виженера"
                font.pixelSize: 26
                font.bold: true
            }
            Label {
                Layout.fillWidth: true
                text: "Ключ-слово задаёт сдвиг для каждой буквы текста."
                wrapMode: Text.WordWrap
            }

            RowLayout {
                spacing: 12
                Label { text: "Алфавит" }
                ComboBox {
                    id: language
                    model: ["Русский", "Английский"]
                    onCurrentIndexChanged: vigenerePractice.resetResult()
                }
                Label { text: "Ключ" }
                TextField {
                    id: key
                    objectName: "keyField"
                    placeholderText: language.currentIndex === 0 ? "Например: КЛЮЧ" : "Например: KEY"
                    selectByMouse: true
                    onTextChanged: vigenerePractice.resetResult()
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
                    onTextChanged: vigenerePractice.resetResult()
                }
            }

            RowLayout {
                Button {
                    text: "Зашифровать"
                    enabled: input.text.length > 0 && key.text.length > 0
                    onClicked: vigenerePractice.process(false)
                }
                Button {
                    text: "Расшифровать"
                    enabled: input.text.length > 0 && key.text.length > 0
                    onClicked: vigenerePractice.process(true)
                }
                Button {
                    text: "Пример"
                    onClicked: {
                        // Ключ и текст примера должны принадлежать выбранному алфавиту.
                        key.text = language.currentIndex === 0 ? "КЛЮЧ" : "KEY"
                        input.text = language.currentIndex === 0 ? "Привет, мир!" : "Hello, world!"
                        vigenerePractice.process(false)
                    }
                }
                Button {
                    text: "Очистить"
                    onClicked: {
                        input.clear()
                        key.clear()
                        vigenerePractice.resetResult()
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
                    text: vigenerePractice.resultText
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
                    text: vigenerePractice.stepsText
                    readOnly: true
                    selectByMouse: true
                    wrapMode: TextEdit.Wrap
                    textFormat: TextEdit.PlainText
                }
            }
        }
    }

    theoryText: "ШИФР ВИЖЕНЕРА\n\n"
        + "Ключ — слово, буквы которого задают сдвиги.\n\n"
        + "1. Пронумеровать буквы алфавита от 0 до N − 1.\n"
        + "2. Повторить ключ до нужного числа букв текста.\n"
        + "3. Взять номера буквы текста x и соответствующей буквы ключа k.\n"
        + "4. Вычислить y = (x + k) mod N и записать новую букву.\n\n"
        + "При расшифровке: x = (y − k) mod N.\n\n"
        + "Пример для английского алфавита: ABC с ключом B превращается в BCD.\n\n"
        + "Повторение короткого ключа создаёт закономерности, помогающие раскрыть шифр."
}
