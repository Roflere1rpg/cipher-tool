"""Рабочая тетрадь: сюда ученик дописывает AES-128.

Начните с aes_course/WORKBOOK.md. Проверка шага: python -m aes_course.checks parse_hex_block
Все числа внутри алгоритма — int, байт — число 0..255.
State — четыре НЕЗАВИСИМЫХ списка строк по четыре числа.
Преобразования возвращают НОВОЕ значение и не меняют входные списки.
Входы внутренних функций считаются корректными; проверку Hex выполняет первая.
Удаляйте raise NotImplementedError только в той функции, которую дописываете.
Не заменяйте его на pass: pass вернёт None и скроет незавершённость задания.
"""

from aes_course.constants import S_BOX, INV_S_BOX, RCON

State = list[list[int]]


def parse_hex_block(text: str) -> bytes:
    """01. Hex → ровно 16 байтов. Пробельные символы разрешены.

    TODO: убрать пробельные символы, проверить 32 Hex-цифры, вернуть bytes.
    Для неверного ввода выбросить ValueError с понятным сообщением.
    Подсказки: str.split, str.join, len, bytes.fromhex. Не обрезать ввод.
    """
    raise NotImplementedError("Шаг 01: parse_hex_block")


def bytes_to_state(block: bytes) -> State:
    """02. TODO: заполнить матрицу по столбцам: state[r][c] = block[4*c+r]."""
    raise NotImplementedError("Шаг 02: bytes_to_state")


def state_to_bytes(state: State) -> bytes:
    """03. TODO: прочитать сверху вниз каждый столбец, вернуть bytes."""
    raise NotImplementedError("Шаг 03: state_to_bytes")


def add_round_key(state: State, round_key: bytes) -> State:
    """04. TODO: XOR каждой клетки с соответствующим байтом ключа.

    round_key — bytes длины 16; порядок байтов такой же, как у блока.
    Python: ^ означает XOR, а ** — возведение в степень.
    """
    raise NotImplementedError("Шаг 04: add_round_key")


def sub_bytes(state: State) -> State:
    """05. TODO: заменить каждое число x на S_BOX[x], позиции сохранить."""
    raise NotImplementedError("Шаг 05: sub_bytes")


def shift_rows(state: State) -> State:
    """06. TODO: строку r циклически сдвинуть влево на r мест (r = 0..3)."""
    raise NotImplementedError("Шаг 06: shift_rows")


def xtime(value: int) -> int:
    """07. TODO: умножение байта на 02 в арифметике AES.

    Запомнить старший бит; сдвинуть влево; оставить 8 бит;
    если старший бит БЫЛ равен 1, применить XOR с 0x1B.
    """
    raise NotImplementedError("Шаг 07: xtime")


def gf_mul(a: int, b: int) -> int:
    """08. TODO: умножение двух байтов в GF(2^8), не обычное a*b.

    Разобрать 8 бит b. На каждом шаге при бите 1 добавить текущее a
    через XOR; перейти от a к xtime(a), от b к b >> 1.
    """
    raise NotImplementedError("Шаг 08: gf_mul")


def mix_columns(state: State) -> State:
    """09. TODO: преобразовать каждый столбец по матрице из тетради.

    Все четыре результата считать из ИСХОДНЫХ четырёх байтов столбца.
    Использовать gf_mul и XOR, сохранить порядок строк и столбцов.
    """
    raise NotImplementedError("Шаг 09: mix_columns")


def rot_word(word: list[int]) -> list[int]:
    """10. TODO: четыре байта [a,b,c,d] → [b,c,d,a]."""
    raise NotImplementedError("Шаг 10: rot_word")


def sub_word(word: list[int]) -> list[int]:
    """11. TODO: заменить четыре байта слова по S_BOX."""
    raise NotImplementedError("Шаг 11: sub_word")


def expand_key(key: bytes) -> list[bytes]:
    """12. TODO: получить список [K0,...,K10], каждый ключ — bytes длины 16.

    Разделить key на 4 слова. Достроить слова с индексами 4..43.
    temp — копия предыдущего слова. Только при i % 4 == 0 применить
    RotWord, SubWord и XOR первого байта с RCON[i//4-1].
    Новое слово — побайтовый XOR слова i-4 и temp.
    Собрать каждые четыре слова в один раундовый ключ. K0 == key.
    """
    raise NotImplementedError("Шаг 12: expand_key")


def encrypt_block(block: bytes, key: bytes) -> bytes:
    """13. TODO: собрать AES-128 из уже проверенных функций.

    Подготовить состояние и ключи; AddRoundKey с K0.
    Раунды 1..9: SubBytes → ShiftRows → MixColumns → AddRoundKey(Kr).
    Раунд 10: SubBytes → ShiftRows → AddRoundKey(K10), затем state_to_bytes.
    Здесь нет кодировки текста, дополнения, IV или режима длинных сообщений.
    """
    raise NotImplementedError("Шаг 13: encrypt_block")


def inv_shift_rows(state: State) -> State:
    """14. TODO: строку r циклически сдвинуть ВПРАВО на r мест."""
    raise NotImplementedError("Шаг 14: inv_shift_rows")


def inv_sub_bytes(state: State) -> State:
    """15. TODO: заменить каждый байт x на INV_S_BOX[x]."""
    raise NotImplementedError("Шаг 15: inv_sub_bytes")


def inv_mix_columns(state: State) -> State:
    """16. TODO: использовать обратную матрицу из тетради и gf_mul."""
    raise NotImplementedError("Шаг 16: inv_mix_columns")


def decrypt_block(block: bytes, key: bytes) -> bytes:
    """17. TODO: собрать обратную последовательность.

    Начало: AddRoundKey(K10).
    Ключи K9..K1: InvShiftRows → InvSubBytes → AddRoundKey → InvMixColumns.
    Конец: InvShiftRows → InvSubBytes → AddRoundKey(K0) → state_to_bytes.
    """
    raise NotImplementedError("Шаг 17: decrypt_block")
