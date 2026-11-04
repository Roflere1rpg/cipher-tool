"""Алгоритмы шифрования. Этот файл ничего не знает об интерфейсе Qt."""

from math import gcd

ENGLISH = "abcdefghijklmnopqrstuvwxyz"
RUSSIAN = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"


def caesar(text: str, shift: int, alphabet: str) -> str:
    """Сдвигает буквы выбранного алфавита, сохраняя регистр.

    Для расшифровки достаточно передать отрицательный сдвиг.
    Пробелы, цифры и символы другого алфавита остаются на месте.
    """
    result = []

    for character in text:
        # Ищем букву без учёта регистра. find вернёт -1, если её нет.
        position = alphabet.find(character.lower())
        if position == -1:
            result.append(character)
            continue

        # Остаток от деления возвращает нас к началу алфавита:
        # для английского z при сдвиге 3 превращается в c.
        new_position = (position + shift) % len(alphabet)
        new_character = alphabet[new_position]

        if character.isupper():
            new_character = new_character.upper()

        result.append(new_character)

    return "".join(result)
def atbash(text: str, alphabet: str) -> str:
    """
    Шифр Атбаш: каждая буква заменяется зеркальной в алфавите.
    """
    result = []
    for character in text:
        position = alphabet.find(character.lower())
        if position == -1:
            result.append(character)
            continue
        new_position = len(alphabet) - 1 - position
        new_character = alphabet[new_position]
        if character.isupper():
            new_character = new_character.upper()
        result.append(new_character)
    return "".join(result)

def vigenere(text: str, key: str, alphabet: str, decrypt: bool = False) -> str:
    """
    Шифр Виженера: ключ-слово задаёт сдвиг для каждой буквы.
    """
    result = []
    key = key.lower()
    # Буква чужого алфавита не задаёт сдвиг. Отклоняем весь ключ,
    # вместо того чтобы незаметно заменять неизвестные буквы нулём.
    if not key or any(character not in alphabet for character in key):
        raise ValueError("Ключ должен содержать только буквы выбранного алфавита.")
    key_index = 0

    for character in text:
        position = alphabet.find(character.lower())
        if position == -1:
            result.append(character)
            continue
        key_char = key[key_index % len(key)]
        key_position = alphabet.find(key_char)

        if decrypt:
            new_position = (position - key_position) % len(alphabet)
        else:
            new_position = (position + key_position) % len(alphabet)

        new_character = alphabet[new_position]
        if character.isupper():
            new_character = new_character.upper()

        result.append(new_character)
        key_index += 1

    return "".join(result)
def affine(text: str, a: int, b: int, alphabet: str, decrypt: bool = False) -> str:
    """
    Аффинный шифр. Формула: y = (a * x + b) mod N.
    Для расшифровки нужно обратное число к a по модулю N.
    """
    n = len(alphabet)
    result = []

    # Проверяем и перед шифрованием: иначе разные буквы могут получить
    # одинаковый результат, и восстановить исходный текст будет невозможно.
    if gcd(a, n) != 1:
        raise ValueError(f"Ключ a должен быть взаимно простым с длиной алфавита ({n}).")

    # Находим обратное число для 'a' (нужно для расшифровки)
    a_inv = -1
    if decrypt:
        for i in range(1, n):
            if (a * i) % n == 1:
                a_inv = i
                break

    for character in text:
        position = alphabet.find(character.lower())
        if position == -1:
            result.append(character)
            continue

        if decrypt:
            # x = a_inv * (y - b) mod N
            new_position = (a_inv * (position - b)) % n
        else:
            # y = (a * x + b) mod N
            new_position = (a * position + b) % n

        new_character = alphabet[new_position]
        if character.isupper():
            new_character = new_character.upper()

        result.append(new_character)
    return "".join(result)
def xor_cipher(text: str, key: str, decrypt: bool = False) -> str:
    """
    Шифр XOR с выводом в Hex-формате.
    """
    result = []
    key_len = len(key)
    if not key:
        raise ValueError("Ключ не может быть пустым.")

    if decrypt:
        # Расшифровка: на вход приходит строка с Hex-кодами (например, "48 65")
        try:
            hex_values = text.split()
            for i, hex_str in enumerate(hex_values):
                # Ожидаем отдельные Hex-числа без знаков и префиксов.
                if any(char not in "0123456789abcdefABCDEF" for char in hex_str):
                    raise ValueError
                k = ord(key[i % key_len])
                char_code = int(hex_str, 16) ^ k
                # Проверяем до chr(): огромное число иначе даёт OverflowError.
                # Суррогаты не являются самостоятельными символами Unicode.
                if not 0 <= char_code <= 0x10FFFF or 0xD800 <= char_code <= 0xDFFF:
                    raise ValueError
                result.append(chr(char_code))
        except ValueError as error:
            raise ValueError("Неверный формат Hex или недопустимый код символа.") from error
        # Пробелы разделяют только Hex-числа. Исходные символы склеиваем
        # без разделителя, сохраняя все пробелы и переносы самого сообщения.
        return "".join(result)
    else:
        # Шифрование: на вход приходит обычный текст
        for i, char in enumerate(text):
            k = ord(key[i % key_len])
            xor_val = ord(char) ^ k
            result.append(f"{xor_val:02x}")

    return " ".join(result)
