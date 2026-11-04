import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ScrollView {
    id: practice
    objectName: "aesPractice"
    contentWidth: availableWidth
    property bool decrypt: direction.currentIndex === 1
    property string resultText: ""
    property string message: "Вычисления ещё не запускались."

    function resetResult() {
        resultText = ""
        message = "Ввод изменён. Запустите обработку заново."
    }

    ColumnLayout {
        width: practice.availableWidth
        spacing: 14
        Label {
            Layout.fillWidth: true
            text: "AES-128: собери шифр по шагам"
            font.pixelSize: 24
            font.bold: true
            wrapMode: Text.WordWrap
        }
        Label {
            Layout.fillWidth: true
            text: "Начните с вкладки «Теория»: там объяснены бит, байт, Hex и XOR. Здесь — 17 небольших заданий. Откройте подсказки, допишите одну функцию в aes_course/student.py, сохраните файл и проверьте шаг. Перезапуск окна не нужен."
            wrapMode: Text.WordWrap
        }
        Label {
            Layout.fillWidth: true
            text: "Маршрут: данные → таблица → XOR → замены и перестановки → смешивание → раундовые ключи → шифрование → обратные операции. Кнопки проверяют заранее известные примеры. «Шаг ещё не готов» — нормальное начало работы."
            wrapMode: Text.WordWrap
        }
        Repeater {
            model: backend.aes_lessons()
            delegate: AesStep {
                required property var modelData
                Layout.fillWidth: true
                lesson: modelData
            }
        }
        GroupBox {
            Layout.fillWidth: true
            title: "Испытание собранного алгоритма · один блок"
            ColumnLayout {
                anchors.fill: parent
                spacing: 10
                Label {
                    Layout.fillWidth: true
                    text: "Эта форма вызывает ваше решение. Пока функции не дописаны, вместо результата появится сообщение о незавершённом шаге."
                    wrapMode: Text.WordWrap
                }
                ComboBox {
                    id: direction
                    objectName: "aesDirection"
                    Layout.fillWidth: true
                    model: ["Шифрование", "Расшифровка"]
                    onCurrentIndexChanged: practice.resetResult()
                }
                Label {
                    Layout.fillWidth: true
                    text: (practice.decrypt ? "Шифроблок" : "Исходный блок") + ": 16 байтов = 32 Hex-цифры"
                    wrapMode: Text.WordWrap
                }
                TextField {
                    id: blockInput
                    objectName: "aesBlock"
                    Layout.fillWidth: true
                    placeholderText: "Hex без 0x; пробелы разрешены"
                    selectByMouse: true
                    onTextChanged: practice.resetResult()
                }
                Label { text: "Ключ: 16 байтов в Hex" }
                TextField {
                    id: keyInput
                    objectName: "aesKey"
                    Layout.fillWidth: true
                    placeholderText: "Ключ из 32 Hex-цифр"
                    selectByMouse: true
                    onTextChanged: practice.resetResult()
                }
                Flow {
                    Layout.fillWidth: true
                    Layout.preferredHeight: childrenRect.height
                    spacing: 8
                    Button {
                        objectName: "aesExample"
                        text: "Контрольный пример"
                        onClicked: {
                            blockInput.text = practice.decrypt
                                ? "3ad77bb40d7a3660a89ecaf32466ef97"
                                : "6bc1bee22e409f96e93d7e117393172a"
                            keyInput.text = "2b7e151628aed2a6abf7158809cf4f3c"
                        }
                    }
                    Button {
                        objectName: "aesRun"
                        text: "Запустить мою реализацию"
                        onClicked: {
                            const answer = backend.process_aes(blockInput.text, keyInput.text, practice.decrypt)
                            practice.resultText = answer.text
                            practice.message = answer.steps
                        }
                    }
                    Button {
                        text: "Очистить"
                        onClicked: {
                            blockInput.clear()
                            keyInput.clear()
                            practice.resetResult()
                        }
                    }
                }
                Label {
                    Layout.fillWidth: true
                    text: "Ожидаемый ответ ТОЛЬКО для контрольного примера: "
                        + (practice.decrypt ? "6bc1bee22e409f96e93d7e117393172a" : "3ad77bb40d7a3660a89ecaf32466ef97")
                    wrapMode: Text.WrapAnywhere
                }
                Label { text: "Фактический результат вашей функции" }
                TextArea {
                    Layout.fillWidth: true
                    text: practice.resultText
                    placeholderText: "Пока результата нет"
                    readOnly: true
                    selectByMouse: true
                    wrapMode: TextEdit.Wrap
                    textFormat: TextEdit.PlainText
                }
                TextArea {
                    Layout.fillWidth: true
                    text: practice.message
                    readOnly: true
                    selectByMouse: true
                    wrapMode: TextEdit.Wrap
                    textFormat: TextEdit.PlainText
                }
            }
        }
    }
}
