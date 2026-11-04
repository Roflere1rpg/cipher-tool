import QtQuick
import "../aes_course/qml"

CipherPage {
    practiceComponent: Component { AesPractice { } }

    theoryMarkdown: true
    theoryText: backend.aes_guide()
}
