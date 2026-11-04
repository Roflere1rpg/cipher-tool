import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    visible: true
    width: 900
    height: 760
    minimumWidth: 660
    minimumHeight: 600
    title: "Шифры — учебное приложение"

    // Сначала выбираем шифр. У каждого — свои практика и теория.
    header: TabBar {
        id: tabs
        TabButton { text: "Цезарь" }
        TabButton { text: "Виженер" }
        TabButton { text: "XOR" }
        TabButton { text: "Атбаш" }
        TabButton { text: "Аффинный" }
        TabButton { text: "AES" }
    }

    // StackLayout показывает только страницу с этим номером.
    StackLayout {
        anchors.fill: parent
        anchors.margins: 24
        currentIndex: tabs.currentIndex

        CaesarPage { }
        VigenerePage { }
        XorPage { }
        AtbashPage { }
        AffinePage { }
        AesPage { }
    }
}
