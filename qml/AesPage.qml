import QtQuick

CipherPage {
    practiceComponent: Component {
        CipherPlaceholder {
            cipherName: "AES"
            description: "Шифрование и расшифровка AES пока недоступны."
        }
    }

    theoryText: "AES\n\n"
        + "Алгоритм AES в приложении пока не реализован.\n\n"
        + "Эта страница подготовлена для будущей реализации шифрования и расшифровки."
}
