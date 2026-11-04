"""Небольшой мост: QML передаёт ввод, Python возвращает результат."""

from PySide6.QtCore import QObject, Slot

from ciphers import ENGLISH, RUSSIAN, caesar, atbash, vigenere, xor_cipher, affine


class Backend(QObject):
    # Slot делает метод доступным из QML. QVariantMap превращает
    # Python-словарь в объект, у которого QML может читать поля.
    @Slot(str, int, str, bool, result="QVariantMap")
    def process_caesar(self, text, shift, language, decrypt):
        """Шифрование и расшифровка Цезаря с пояснением замен."""
        alphabet = RUSSIAN if language == "Русский" else ENGLISH
        actual_shift = -shift if decrypt else shift
        result = caesar(text, actual_shift, alphabet)

        # Показываем несколько замен, чтобы пояснение не росло
        # вместе с большим текстом. Сам текст обрабатывается целиком.
        steps = []
        for before, after in zip(text, result):
            position = alphabet.find(before.lower())
            if position != -1:
                new_position = (position + actual_shift) % len(alphabet)
                steps.append(
                    f"{before} → {after}: ({position} + ({actual_shift})) "
                    f"mod {len(alphabet)} = {new_position}"
                )
            if len(steps) == 12:
                break

        return {
            "text": result,
            "steps": "\n".join(steps) or "Введите буквы выбранного алфавита.",
        }

    @Slot(str, str, result="QVariantMap")
    def process_atbash(self, text, language):
        alphabet = RUSSIAN if language == "Русский" else ENGLISH
        result = atbash(text, alphabet)
        return {
            "text": result,
            "steps": f"Атбаш: буквы заменены зеркально\nРезультат: {result}"
        }

    @Slot(str, str, str, bool, result="QVariantMap")
    def process_vigenere(self, text, key, language, decrypt):
        alphabet = RUSSIAN if language == "Русский" else ENGLISH
        if not key or not key.isalpha():
            return {
                "text": "",
                "steps": "Ошибка: ключ должен состоять только из букв."
            }
        result = vigenere(text, key, alphabet, decrypt)
        action = "Расшифровка" if decrypt else "Шифрование"
        return {
            "text": result,
            "steps": f"{action} Виженера\nКлюч: {key}\nРезультат: {result}"
        }
    @Slot(str, int, int, str, bool, result="QVariantMap")
    def process_affine(self, text, a, b, language, decrypt):
        alphabet = RUSSIAN if language == "Русский" else ENGLISH
        result = affine(text, a, b, alphabet, decrypt)
        action = "Расшифровка" if decrypt else "Шифрование"
        return {
            "text": result,
            "steps": f"{action} Аффинного шифра\nКлючи: a={a}, b={b}\nРезультат: {result}"
        }
    @Slot(str, str, bool, result="QVariantMap")
    def process_xor(self, text, key, decrypt):
        if not key:
            return {"text": "", "steps": "Ошибка: ключ не может быть пустым."}
        result = xor_cipher(text, key, decrypt)
        action = "Расшифровка" if decrypt else "Шифрование"
        return {
            "text": result,
            "steps": f"{action} XOR\nКлюч: {key}\nРезультат: {result}"
        }
    @Slot(str, str, bool, result="QVariantMap")
    def process_aes(self, text, key, decrypt):
        """Заготовка для будущего алгоритма AES: результат пока отсутствует."""
        return {
            "text": "",
            "steps": "AES пока не реализован. Шифрование и расшифровка недоступны."
        }
