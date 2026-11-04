"""Алгоритмы шифрования. Этот файл ничего не знает об интерфейсе Qt."""

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
    key_index = 0

    for character in text:
        position = alphabet.find(character.lower())
        if position == -1:
            result.append(character)
            continue
        key_char = key[key_index % len(key)]
        key_position = alphabet.find(key_char)
        if key_position == -1:
            key_position = 0

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

    # Находим обратное число для 'a' (нужно для расшифровки)
    a_inv = -1
    if decrypt:
        for i in range(1, n):
            if (a * i) % n == 1:
                a_inv = i
                break
        if a_inv == -1:
            return "Ошибка: для этого 'a' нет обратного числа. Выберите другое 'a' (например, 5, 7, 11)."

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

    if decrypt:
        # Расшифровка: на вход приходит строка с Hex-кодами (например, "48 65")
        try:
            hex_values = text.split()
            for i, hex_str in enumerate(hex_values):
                k = ord(key[i % key_len])
                char_code = int(hex_str, 16) ^ k 
                result.append(chr(char_code))
        except ValueError:
            return "Ошибка: неверный формат Hex."
    else:
        # Шифрование: на вход приходит обычный текст
        for i, char in enumerate(text):
            k = ord(key[i % key_len])
            xor_val = ord(char) ^ k
            result.append(f"{xor_val:02x}")

    return " ".join(result)
def aes_encrypt(text: str, key: str) -> str:
    key_bytes = key.encode('utf-8')[:16].ljust(16, b'\0')
    text_bytes = text.encode('utf-8')
    padded_text = text_bytes.ljust((len(text_bytes) + 15) // 16 * 16, b'\0')
    
    result = []
    for i in range(0, len(padded_text), 16):
        block = padded_text[i:i+16]
        encrypted_block = _aes_process_block(block, key_bytes)
        result.append(encrypted_block)
    
    return " ".join([b.hex() for b in result])

def _aes_process_block(block, key):
    result = bytearray(16)
    for i in range(16):
        result[i] = block[i] ^ key[i]
    return bytes(result)