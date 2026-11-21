import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ScrollView {
    id: page
    objectName: "aesPage"
    contentWidth: availableWidth
    property var trace: []
    property var roundKeys: []
    property int selectedStep: 0
    property string resultText: ""
    property string message: ""
    property bool hasError: false
    readonly property var currentStep: trace.length ? trace[selectedStep] : null
    readonly property bool decrypt: direction.currentIndex === 1

    function resetResult() {
        trace = []
        roundKeys = []
        selectedStep = 0
        resultText = ""
        message = ""
        hasError = false
    }

    function process() {
        const answer = backend.process_aes(blockInput.text, keyInput.text, decrypt)
        // Сначала сбрасываем индекс: новый ответ может иметь другую длину.
        selectedStep = 0
        trace = answer.steps
        roundKeys = answer.roundKeys
        resultText = answer.text
        message = answer.message
        hasError = answer.status === "error"
    }

    ColumnLayout {
        width: page.availableWidth
        spacing: 14

        Label {
            text: "AES-128"
            font.pixelSize: 26
            font.bold: true
        }
        Label {
            Layout.fillWidth: true
            text: "Шифрование и расшифровка одного блока · 10 раундов · просмотр всех преобразований"
            wrapMode: Text.WordWrap
        }
        Frame {
            Layout.fillWidth: true
            ColumnLayout {
                anchors.fill: parent
                spacing: 10
                ComboBox {
                    id: direction
                    objectName: "aesDirection"
                    Layout.fillWidth: true
                    model: ["Шифрование", "Расшифровка"]
                    onCurrentIndexChanged: page.resetResult()
                }
                Label {
                    Layout.fillWidth: true
                    text: (page.decrypt ? "Шифроблок" : "Исходный блок") + " · 16 байтов в Hex"
                    wrapMode: Text.WordWrap
                }
                TextField {
                    id: blockInput
                    objectName: "aesBlock"
                    Layout.fillWidth: true
                    placeholderText: "32 Hex-цифры; пробелы разрешены"
                    font.family: "Consolas"
                    selectByMouse: true
                    onTextChanged: page.resetResult()
                }
                Label { text: "Ключ AES-128 · 16 байтов в Hex" }
                TextField {
                    id: keyInput
                    objectName: "aesKey"
                    Layout.fillWidth: true
                    placeholderText: "32 Hex-цифры, без префикса 0x"
                    font.family: "Consolas"
                    selectByMouse: true
                    onTextChanged: page.resetResult()
                }
                Flow {
                    Layout.fillWidth: true
                    Layout.preferredHeight: childrenRect.height
                    spacing: 8
                    Button {
                        objectName: "aesRun"
                        text: page.decrypt ? "Расшифровать" : "Зашифровать"
                        highlighted: true
                        onClicked: page.process()
                    }
                    Button {
                        objectName: "aesExample"
                        text: "Пример"
                        onClicked: {
                            blockInput.text = page.decrypt
                                ? "3ad77bb40d7a3660a89ecaf32466ef97"
                                : "6bc1bee22e409f96e93d7e117393172a"
                            keyInput.text = "2b7e151628aed2a6abf7158809cf4f3c"
                            page.resetResult()
                        }
                    }
                    Button {
                        text: "Очистить"
                        onClicked: {
                            blockInput.clear()
                            keyInput.clear()
                            page.resetResult()
                        }
                    }
                }
                Label {
                    Layout.fillWidth: true
                    visible: page.message.length > 0
                    text: page.message
                    color: page.hasError ? "#b42318" : palette.text
                    wrapMode: Text.WordWrap
                }
            }
        }

        GroupBox {
            Layout.fillWidth: true
            visible: page.resultText.length > 0
            title: page.decrypt ? "Расшифрованный блок" : "Шифроблок"
            ColumnLayout {
                anchors.fill: parent
                TextField {
                    objectName: "aesResult"
                    Layout.fillWidth: true
                    text: page.resultText
                    readOnly: true
                    selectByMouse: true
                    font.family: "Consolas"
                }
                Button {
                    objectName: "aesReverse"
                    text: page.decrypt ? "Зашифровать результат" : "Расшифровать результат"
                    onClicked: {
                        const value = page.resultText
                        direction.currentIndex = page.decrypt ? 0 : 1
                        blockInput.text = value
                        page.process()
                    }
                }
            }
        }

        GroupBox {
            Layout.fillWidth: true
            visible: page.trace.length > 0
            title: "Преобразования по шагам"
            ColumnLayout {
                anchors.fill: parent
                spacing: 12
                ComboBox {
                    id: stepSelector
                    objectName: "aesStepSelector"
                    Layout.fillWidth: true
                    model: page.trace
                    textRole: "title"
                    currentIndex: page.selectedStep
                    onActivated: function(index) { page.selectedStep = index }
                }
                RowLayout {
                    Layout.fillWidth: true
                    Button {
                        objectName: "aesPrevious"
                        text: "← Назад"
                        enabled: page.selectedStep > 0
                        onClicked: page.selectedStep--
                    }
                    Label {
                        Layout.fillWidth: true
                        horizontalAlignment: Text.AlignHCenter
                        text: "Шаг " + (page.selectedStep + 1) + " из " + page.trace.length
                    }
                    Button {
                        objectName: "aesNext"
                        text: "Далее →"
                        enabled: page.selectedStep + 1 < page.trace.length
                        onClicked: page.selectedStep++
                    }
                }
                Label {
                    Layout.fillWidth: true
                    text: page.currentStep ? page.currentStep.description : ""
                    wrapMode: Text.WordWrap
                }
                RowLayout {
                    Layout.fillWidth: true
                    spacing: 16
                    AesState {
                        Layout.fillWidth: true
                        Layout.preferredWidth: 1
                        title: "До операции"
                        cells: page.currentStep ? page.currentStep.before : []
                    }
                    AesState {
                        Layout.fillWidth: true
                        Layout.preferredWidth: 1
                        title: "После операции"
                        cells: page.currentStep ? page.currentStep.after : []
                        comparison: page.currentStep ? page.currentStep.before : []
                        highlightChanges: true
                    }
                }
                Label {
                    Layout.fillWidth: true
                    text: "Зелёным выделены изменившиеся значения. Блок читается по столбцам сверху вниз."
                    wrapMode: Text.WordWrap
                }
                TextField {
                    Layout.fillWidth: true
                    text: page.currentStep ? page.currentStep.afterHex : ""
                    font.family: "Consolas"
                    readOnly: true
                    selectByMouse: true
                }
                AesState {
                    Layout.fillWidth: true
                    Layout.maximumWidth: 280
                    visible: page.currentStep ? page.currentStep.keyLabel.length > 0 : false
                    title: page.currentStep ? "Раундовый ключ · " + page.currentStep.keyLabel : ""
                    cells: page.currentStep ? page.currentStep.keyCells : []
                }
                TextField {
                    Layout.fillWidth: true
                    visible: page.currentStep ? page.currentStep.keyLabel.length > 0 : false
                    text: page.currentStep ? page.currentStep.keyHex : ""
                    font.family: "Consolas"
                    readOnly: true
                    selectByMouse: true
                }
            }
        }
        GroupBox {
            Layout.fillWidth: true
            visible: page.roundKeys.length > 0
            title: "Раундовые ключи · K0–K10"
            ColumnLayout {
                anchors.fill: parent
                spacing: 8
                Label {
                    Layout.fillWidth: true
                    text: "KeyExpansion вычисляет все ключи заранее. K0 — исходный ключ. "
                        + (page.decrypt ? "Расшифровка использует ключи в порядке K10 → K0."
                                        : "Шифрование использует ключи в порядке K0 → K10.")
                        + " Расчёт K1 разобран во вкладке «Теория»."
                    wrapMode: Text.WordWrap
                }
                Repeater {
                    model: page.roundKeys
                    delegate: RowLayout {
                        required property var modelData
                        Layout.fillWidth: true
                        Label { text: modelData.label; Layout.preferredWidth: 30 }
                        TextField {
                            Layout.fillWidth: true
                            text: modelData.hex
                            font.family: "Consolas"
                            readOnly: true
                            selectByMouse: true
                        }
                    }
                }
            }
        }
    }
}
