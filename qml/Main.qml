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

    header: TabBar {
        id: categories
        objectName: "cipherCategories"
        TabButton { text: "Симметричные" }
        TabButton { text: "Асимметричные" }
        TabButton { text: "Сравнение" }
    }

    StackLayout {
        anchors.fill: parent
        anchors.margins: 24
        currentIndex: categories.currentIndex

        ColumnLayout {
            spacing: 16
            TabBar {
                id: symmetricTabs
                objectName: "symmetricCiphers"
                Layout.fillWidth: true
                TabButton { text: "Цезарь" }
                TabButton { text: "Виженер" }
                TabButton { text: "XOR" }
                TabButton { text: "Атбаш" }
                TabButton { text: "Аффинный" }
                TabButton { text: "AES" }
            }
            StackLayout {
                Layout.fillWidth: true
                Layout.fillHeight: true
                currentIndex: symmetricTabs.currentIndex

                CaesarPage { }
                VigenerePage { }
                XorPage { }
                AtbashPage { }
                AffinePage { }
                AesPage { }
            }
        }

        TheoryPage {
            objectName: "asymmetricOverview"
            text: "АСИММЕТРИЧНОЕ ШИФРОВАНИЕ\n\n"
                + "У получателя есть два связанных ключа. Открытый можно передать кому угодно. Закрытый хранит только получатель.\n\n"
                + "1. Получатель передаёт отправителю свой открытый ключ.\n"
                + "2. Отправитель шифрует данные открытым ключом получателя.\n"
                + "3. Получатель расшифровывает данные своим закрытым ключом.\n\n"
                + "Пример такого алгоритма — RSA. Перед шифрованием важно убедиться, что открытый ключ действительно принадлежит получателю.\n\n"
                + "Откройте «Сравнение», чтобы увидеть, чем эта схема отличается от AES и зачем их используют вместе."
        }

        TheoryPage {
            objectName: "cipherComparison"
            text: "СИММЕТРИЧНЫЕ И АСИММЕТРИЧНЫЕ ШИФРЫ\n\n"
                + "Симметричное шифрование · один общий секрет\n"
                + "Один и тот же секретный ключ нужен для шифрования и расшифровки. Отправителю и получателю нужно заранее безопасно получить общий ключ. Пример — AES.\n\n"
                + "Асимметричное шифрование · пара ключей\n"
                + "Для шифрования нужен открытый ключ получателя, для расшифровки — его закрытый ключ. Отправителю достаточно получить подлинный открытый ключ. Пример — RSA.\n\n"
                + "Как их используют вместе\n"
                + "Симметричное шифрование обычно быстрее и подходит для больших объёмов данных. Асимметрические методы могут помочь сторонам безопасно установить общий ключ, а симметрический алгоритм затем шифрует данные.\n\n"
                + "Рядом с AES в разделе «Симметричные» собраны классические учебные шифры. Атбаш — фиксированная замена букв без секретного ключа."
        }
    }
}
