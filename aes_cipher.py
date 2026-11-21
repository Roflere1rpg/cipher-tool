"""AES-128: ??????????? ?????????? ???????? ?? 21.11.26.

?????????????? ?????????; ????????? ?????? ????????????? ????????? ??? ??????????.
???????? ?????? ???????? ? ????? aes_course.
"""

from aes_constants import S_BOX, INV_S_BOX, RCON

# 01. Превращаем Hex в байты
def parse_hex_block(hex_str):
    # Сначала убери пробелы табуляции и переносы
    clean_str = "".join(hex_str.split())

    # Проверь, что осталось ровно 32 символа
    if len(clean_str) != 32:
        raise ValueError("Длина Hex-строки должна быть ровно 32 символа (16 байт).")

    # Проверь, что каждый — цифра 0…9 или буква a…f (регистр не важен)
    for char in clean_str.lower():
        if char not in "0123456789abcdef":
            raise ValueError(f"Недопустимый символ в Hex-строке: {char}")

    # Преобразуй в байты
    return bytes.fromhex(clean_str)

# 02. Раскладываем байты в таблицу
def bytes_to_state(block):
    state = []
    for r in range(4):
        row = []
        for c in range(4):
            # Байт для клетки (r, c) имеет номер 4*c+r
            row.append(block[4 * c + r])
        state.append(row)
    return state

# 03. Собираем таблицу обратно
def state_to_bytes(state):
    result = []
    for c in range(4):
        for r in range(4):
            result.append(state[r][c])
    return bytes(result)

# 04. Знакомимся с XOR и накладываем ключ
def add_round_key(state, round_key):
    key_state = bytes_to_state(round_key)
    new_state = []
    for r in range(4):
        row = []
        for c in range(4):
            row.append(state[r][c] ^ key_state[r][c])
        new_state.append(row)
    return new_state

# 05. Заменяем значения по справочнику
def sub_bytes(state):
    new_state = []
    for r in range(4):
        row = []
        for c in range(4):
            row.append(S_BOX[state[r][c]])
        new_state.append(row)
    return new_state

# 06. Переставляем клетки строк
def shift_rows(state):
    new_state = []
    for r in range(4):
        row = []
        for c in range(4):
            row.append(state[r][(c + r) % 4])
        new_state.append(row)
    return new_state

# 07. Учим особое умножение на два
def xtime(value):
    if value & 0x80:
        return ((value << 1) & 0xFF) ^ 0x1B
    else:
        return (value << 1) & 0xFF

# 08. Умножаем два байта
def gf_mul(a, b):
    result = 0
    for _ in range(8):
        if b & 1:
            result ^= a
        a = xtime(a)
        b >>= 1
    return result

# 09. Смешиваем четыре числа столбца
def mix_columns(state):
    new_state = [[0]*4 for _ in range(4)]
    for c in range(4):
        a = state[0][c]
        b = state[1][c]
        col_c = state[2][c]
        d = state[3][c]

        new_state[0][c] = gf_mul(a, 0x02) ^ gf_mul(b, 0x03) ^ col_c ^ d
        new_state[1][c] = a ^ gf_mul(b, 0x02) ^ gf_mul(col_c, 0x03) ^ d
        new_state[2][c] = a ^ b ^ gf_mul(col_c, 0x02) ^ gf_mul(d, 0x03)
        new_state[3][c] = gf_mul(a, 0x03) ^ b ^ col_c ^ gf_mul(d, 0x02)
    return new_state

# 10. Поворачиваем слово ключа
def rot_word(word):
    return word[1:] + word[:1]

# 11. Заменяем байты слова ключа
def sub_word(word):
    return [S_BOX[b] for b in word]

# 12. Готовим одиннадцать раундовых ключей
def expand_key(key):
    # Разбиваем на 4 слова по 4 байта
    w = [list(key[i:i+4]) for i in range(0, 16, 4)]

    for i in range(4, 44):
        temp = w[i-1].copy() # Важно делать копию!

        if i % 4 == 0:
            temp = rot_word(temp)
            temp = sub_word(temp)
            temp[0] ^= RCON[i // 4 - 1]

        new_word = [w[i-4][j] ^ temp[j] for j in range(4)]
        w.append(new_word)

    # Собираем обратно в байты
    round_keys = []
    for i in range(11):
        rk = []
        for j in range(4):
            rk.extend(w[i*4 + j])
        round_keys.append(bytes(rk))
    return round_keys

# 13. Собираем шифрование
def _record(trace, operation, round_number, state, key_index=None, keys=None):
    """Снимок независим от дальнейших изменений: интерфейс только читает его."""
    if trace is not None:
        trace.append({"operation": operation, "round": round_number,
                      "state": [row.copy() for row in state], "keyIndex": key_index,
                      "keys": list(keys) if keys is not None else None})


def _validate_block(block, key):
    if not isinstance(block, bytes) or len(block) != 16:
        raise ValueError("Блок должен содержать ровно 16 байтов.")
    if not isinstance(key, bytes) or len(key) != 16:
        raise ValueError("Ключ AES-128 должен содержать ровно 16 байтов.")


def encrypt_block(block, key, trace=None):
    _validate_block(block, key)
    round_keys = expand_key(key)
    state = bytes_to_state(block)
    _record(trace, "Input", 0, state)
    _record(trace, "KeyExpansion", 0, state, keys=round_keys)

    # Начальное AddRoundKey
    state = add_round_key(state, round_keys[0])
    _record(trace, "AddRoundKey", 0, state, 0)

    # 9 полных раундов
    for r in range(1, 10):
        state = sub_bytes(state)
        _record(trace, "SubBytes", r, state)
        state = shift_rows(state)
        _record(trace, "ShiftRows", r, state)
        state = mix_columns(state)
        _record(trace, "MixColumns", r, state)
        state = add_round_key(state, round_keys[r])
        _record(trace, "AddRoundKey", r, state, r)

    # 10-й раунд (без MixColumns)
    state = sub_bytes(state)
    _record(trace, "SubBytes", 10, state)
    state = shift_rows(state)
    _record(trace, "ShiftRows", 10, state)
    state = add_round_key(state, round_keys[10])
    _record(trace, "AddRoundKey", 10, state, 10)

    return state_to_bytes(state)

# 14. Возвращаем строки на место
def inv_shift_rows(state):
    new_state = []
    for r in range(4):
        row = []
        for c in range(4):
            row.append(state[r][(c - r) % 4])
        new_state.append(row)
    return new_state

# 15. Возвращаем исходные значения байтов
def inv_sub_bytes(state):
    new_state = []
    for r in range(4):
        row = []
        for c in range(4):
            row.append(INV_S_BOX[state[r][c]])
        new_state.append(row)
    return new_state

# 16. Отменяем смешивание столбцов
def inv_mix_columns(state):
    new_state = [[0]*4 for _ in range(4)]
    for c in range(4):
        a = state[0][c]
        b = state[1][c]
        col_c = state[2][c]
        d = state[3][c]

        new_state[0][c] = gf_mul(a, 0x0e) ^ gf_mul(b, 0x0b) ^ gf_mul(col_c, 0x0d) ^ gf_mul(d, 0x09)
        new_state[1][c] = gf_mul(a, 0x09) ^ gf_mul(b, 0x0e) ^ gf_mul(col_c, 0x0b) ^ gf_mul(d, 0x0d)
        new_state[2][c] = gf_mul(a, 0x0d) ^ gf_mul(b, 0x09) ^ gf_mul(col_c, 0x0e) ^ gf_mul(d, 0x0b)
        new_state[3][c] = gf_mul(a, 0x0b) ^ gf_mul(b, 0x0d) ^ gf_mul(col_c, 0x09) ^ gf_mul(d, 0x0e)
    return new_state

# 17. Собираем расшифровку
def decrypt_block(block, key, trace=None):
    _validate_block(block, key)
    round_keys = expand_key(key)
    state = bytes_to_state(block)
    _record(trace, "Input", 0, state)
    _record(trace, "KeyExpansion", 0, state, keys=round_keys)

    # Начинаем с K10
    state = add_round_key(state, round_keys[10])
    _record(trace, "AddRoundKey", 0, state, 10)

    # Раунды 9...1
    for r in range(9, 0, -1):
        state = inv_shift_rows(state)
        _record(trace, "InvShiftRows", 10-r, state)
        state = inv_sub_bytes(state)
        _record(trace, "InvSubBytes", 10-r, state)
        state = add_round_key(state, round_keys[r])
        _record(trace, "AddRoundKey", 10-r, state, r)
        state = inv_mix_columns(state)
        _record(trace, "InvMixColumns", 10-r, state)

    # Финал
    state = inv_shift_rows(state)
    _record(trace, "InvShiftRows", 10, state)
    state = inv_sub_bytes(state)
    _record(trace, "InvSubBytes", 10, state)
    state = add_round_key(state, round_keys[0])
    _record(trace, "AddRoundKey", 10, state, 0)

    return state_to_bytes(state)
