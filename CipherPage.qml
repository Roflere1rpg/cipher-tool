import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

// Общая структура. Каждый шифр задаёт свою форму практики и справку.
ColumnLayout {
    id: page
    property Component practiceComponent
    property string theoryText: ""
    spacing: 16

    TabBar {
        id: sections
        Layout.fillWidth: true
        TabButton { text: "Практика" }
        TabButton { text: "Теория" }
    }

    // Страницы остаются в памяти: переключение не сбрасывает ввод.
    StackLayout {
        Layout.fillWidth: true
        Layout.fillHeight: true
        currentIndex: sections.currentIndex

        Loader { sourceComponent: page.practiceComponent }
        TheoryPage { text: page.theoryText }
    }
}
