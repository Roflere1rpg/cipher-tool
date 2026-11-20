import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

// Карточка проверяет только один шаг на заранее известных входах.
// Контрольные примеры не зависят от введённого внизу страницы блока.
Frame {
    id: step
    property var lesson
    property string feedback: "Пока не проверено."
    property string status: "idle"
    objectName: "aesStep_" + lesson.id

    ColumnLayout {
        anchors.fill: parent
        spacing: 8
        Label {
            Layout.fillWidth: true
            text: step.lesson.title
            font.bold: true
            font.pixelSize: 18
            wrapMode: Text.WordWrap
        }
        Label {
            Layout.fillWidth: true
            text: step.lesson.summary
            wrapMode: Text.WordWrap
        }
        Label {
            Layout.fillWidth: true
            text: "Допишите " + step.lesson.id + " в aes_course/student.py"
            wrapMode: Text.WrapAnywhere
        }
        CheckBox {
            id: explanationToggle
            text: "Объяснение, пример и подсказки"
            checked: false
        }
        TextArea {
            Layout.fillWidth: true
            visible: explanationToggle.checked
            readOnly: true
            selectByMouse: true
            textFormat: TextEdit.PlainText
            wrapMode: TextEdit.Wrap
            text: step.lesson.explanation
        }
        Button {
            objectName: "check_" + step.lesson.id
            text: "Проверить шаг"
            onClicked: {
                const answer = backend.check_aes_step(step.lesson.id)
                step.status = answer.status
                step.feedback = answer.steps
            }
        }
        Label {
            Layout.fillWidth: true
            font.bold: true
            text: step.status === "passed" ? "Проверено на контрольных примерах"
                : step.status === "pending" ? "Шаг ещё не готов"
                : step.status === "error" ? "Нужно исправить" : "Ожидает проверки"
            wrapMode: Text.WordWrap
        }
        TextArea {
            Layout.fillWidth: true
            readOnly: true
            selectByMouse: true
            wrapMode: TextEdit.Wrap
            textFormat: TextEdit.PlainText
            text: step.feedback
        }
    }
}
