import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

CipherPage {
    practiceComponent: Component {
        ColumnLayout {
            id: atbashPractice
            spacing: 10

            property string resultText: ""
            property string stepsText: "Здесь появится результат."

            function resetResult() {
                resultText = ""
                stepsText = "Здесь появится результат."
            }

            function process() {
                const answer = backend.process_atbash(input.text, language.currentText)
                resultText = answer.text
                stepsText = answer.steps
            }

            Label {
                text: "Шифр Атбаш"
                font.pixelSize: 26
                font.bold: true
            }
            Label {
                Layout.fillWidth: true
                text: "Зеркальная замена букв алфавита без секретного ключа."
                wrapMode: Text.WordWrap
            }

            RowLayout {
                spacing: 12
                Label { text: "Алфавит" }
                ComboBox {
                    id: language
                    model: ["Русский", "Английский"]
                    onCurrentIndexChanged: atbashPractice.resetResult()
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
                    onTextChanged: atbashPractice.resetResult()
                }
            }

            RowLayout {
                Button {
                    text: "Зашифровать"
                    enabled: input.text.length > 0
                    onClicked: atbashPractice.process()
                }
                Button {
                    text: "Расшифровать"
                    enabled: input.text.length > 0
                    onClicked: atbashPractice.process()
                }
                Button {
                    text: "Пример"
                    onClicked: {
                        input.text = language.currentIndex === 0 ? "Привет, мир!" : "Hello, world!"
                        atbashPractice.process()
                    }
                }
                Button {
                    text: "Очистить"
                    onClicked: {
                        input.clear()
                        atbashPractice.resetResult()
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
                    text: atbashPractice.resultText
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
                    text: atbashPractice.stepsText
                    readOnly: true
                    selectByMouse: true
                    wrapMode: TextEdit.Wrap
                    textFormat: TextEdit.PlainText
                }
            }
        }
    }

    theoryText: "ШИФР АТБАШ\n\n"
        + "Первая буква заменяется последней, вторая — предпоследней и так далее.\n\n"
        + "1. Выбрать алфавит из N букв.\n"
        + "2. Найти номер буквы x, начиная с нуля.\n"
        + "3. Вычислить зеркальный номер y = N − 1 − x.\n"
        + "4. Записать букву с номером y.\n\n"
        + "Повторное применение той же замены расшифровывает текст.\n\n"
        + "Пример для английского алфавита: ABC → ZYX → ABC.\n\n"
        + "Секретного ключа нет: зная способ замены и алфавит, можно сразу прочитать сообщение."
}