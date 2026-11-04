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
        + "Это обобщение шифра Цезаря. Каждая буква x заменяется на y = (a * x + b) mod N.\n\n"
        + "1. 'a' и 'b' — ключи.\n"
        + "2. 'a' должно быть взаимно простым с размером алфавита N (не иметь общих делителей, кроме 1). Для английского N=26, поэтому 'a' может быть 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25.\n"
        + "3. Для расшифровки используется обратное число к 'a'.\n\n"
        + "Пример: a=5, b=8. 'A'(0) -> (5*0+8) mod 26 = 8 ('I')."
}