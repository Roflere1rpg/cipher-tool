import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

CipherPage {
    practiceComponent: Component {
        ColumnLayout {
            id: affinePractice
            spacing: 10

            property string resultText: ""
            property string stepsText: "Здесь появится результат."

            function resetResult() {
                resultText = ""
                stepsText = "Здесь появится результат."
            }

            function process(decrypt) {
                const answer = backend.process_affine(input.text, aSpin.value, bSpin.value, language.currentText, decrypt)
                resultText = answer.text
                stepsText = answer.steps
            }

            Label {
                text: "Аффинный шифр"
                font.pixelSize: 26
                font.bold: true
            }
            Label {
                Layout.fillWidth: true
                text: "Формула: y = (a * x + b) mod 26. 'a' должно быть взаимно простым с размером алфавита."
                wrapMode: Text.WordWrap
            }

            RowLayout {
                spacing: 12
                Label { text: "Алфавит" }
                ComboBox {
                    id: language
                    model: ["Русский", "Английский"]
                    onCurrentIndexChanged: affinePractice.resetResult()
                }
                Label { text: "Ключ a" }
                SpinBox {
                    id: aSpin
                    from: 1
                    to: language.currentIndex === 0 ? 32 : 25
                    value: 5
                    onValueChanged: affinePractice.resetResult()
                }
                Label { text: "Ключ b" }
                SpinBox {
                    id: bSpin
                    from: 0
                    to: language.currentIndex === 0 ? 32 : 25
                    value: 3
                    onValueChanged: affinePractice.resetResult()
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
                    placeholderText: "Например: Hello, world!"
                    wrapMode: TextEdit.Wrap
                    textFormat: TextEdit.PlainText
                    selectByMouse: true
                    onTextChanged: affinePractice.resetResult()
                }
            }

            RowLayout {
                Button {
                    text: "Зашифровать"
                    enabled: input.text.length > 0
                    onClicked: affinePractice.process(false)
                }
                Button {
                    text: "Расшифровать"
                    enabled: input.text.length > 0
                    onClicked: affinePractice.process(true)
                }
                Button {
                    text: "Пример"
                    onClicked: {
                        aSpin.value = 5
                        bSpin.value = 8
                        input.text = "Hello, world!"
                        affinePractice.process(false)
                    }
                }
                Button {
                    text: "Очистить"
                    onClicked: {
                        input.clear()
                        affinePractice.resetResult()
                    }
                }
            }

            Label { text: "Результат" }
            ScrollView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.minimumHeight: 80
                contentWidth: availableWidth
                TextArea {
                    objectName: "resultText"
                    text: affinePractice.resultText
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
                    text: affinePractice.stepsText
                    readOnly: true
                    selectByMouse: true
                    wrapMode: TextEdit.Wrap
                    textFormat: TextEdit.PlainText
                }
            }
        }
    }

    theoryText: "АФФИННЫЙ ШИФР\n\n"
        + "Ключ состоит из чисел a и b. N — длина выбранного алфавита.\n\n"
        + "1. Проверить, что a и N взаимно просты: их общий делитель только 1.\n"
        + "2. Найти номер буквы x, начиная с нуля.\n"
        + "3. Вычислить y = (a·x + b) mod N.\n"
        + "4. Заменить исходную букву буквой с номером y.\n\n"
        + "Для расшифровки найти число a⁻¹, для которого (a·a⁻¹) mod N = 1. "
        + "Тогда x = a⁻¹·(y − b) mod N.\n\n"
        + "Пример: при N = 26, a = 5 и b = 8 текст ABC превращается в INS.\n\n"
        + "Это постоянная замена букв: частоты букв сохраняются, что помогает анализировать шифртекст."
}
