"""Учебные проверки без реализации AES. Запуск: python -m aes_course.checks [имя_шага].

Входы каждого этапа уже подготовлены: незавершённые соседние этапы не мешают
проверке. Ожидаемые ответы — константы, а не вычисления функциями ученика.
"""

import argparse
import importlib
import sys
from copy import deepcopy

from aes_course.lessons import LESSONS

BLOCK_HEX = "6bc1bee22e409f96e93d7e117393172a"
KEY_HEX = "2b7e151628aed2a6abf7158809cf4f3c"
CIPHER_HEX = "3ad77bb40d7a3660a89ecaf32466ef97"
BLOCK, KEY, CIPHER = map(bytes.fromhex, (BLOCK_HEX, KEY_HEX, CIPHER_HEX))

# Матрицы записаны строками, а Hex-значения NIST — по столбцам.
GRID = [[0, 4, 8, 12], [1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15]]
SHIFTED_GRID = [[0, 4, 8, 12], [5, 9, 13, 1], [10, 14, 2, 6], [15, 3, 7, 11]]
START = [[0x6b, 0x2e, 0xe9, 0x73], [0xc1, 0x40, 0x3d, 0x93],
         [0xbe, 0x9f, 0x7e, 0x17], [0xe2, 0x96, 0x11, 0x2a]]
ADDED = [[0x40, 0x06, 0x42, 0x7a], [0xbf, 0xee, 0xca, 0x5c],
         [0xab, 0x4d, 0x6b, 0x58], [0xf4, 0x30, 0x99, 0x16]]
SUBBED = [[0x09, 0x6f, 0x2c, 0xda], [0x08, 0x28, 0x74, 0x4a],
          [0x62, 0xe3, 0x7f, 0x6a], [0xbf, 0x04, 0xee, 0x47]]
SHIFTED = [[0x09, 0x6f, 0x2c, 0xda], [0x28, 0x74, 0x4a, 0x08],
           [0x7f, 0x6a, 0x62, 0xe3], [0x47, 0xbf, 0x04, 0xee]]
MIXED = [[0x52, 0x97, 0xe0, 0xba], [0x9f, 0x86, 0x1a, 0x1a],
         [0x16, 0x15, 0xae, 0x26], [0xc2, 0xca, 0x54, 0x59]]
ROUND_ONE = [[0xf2, 0x1f, 0xc3, 0x90], [0x65, 0xd2, 0xb9, 0x76],
             [0xe8, 0x39, 0x97, 0x50], [0xd5, 0x7b, 0x6d, 0x5c]]
KEYS = [bytes.fromhex(value) for value in (
    KEY_HEX, "a0fafe1788542cb123a339392a6c7605", "f2c295f27a96b9435935807a7359f67f",
    "3d80477d4716fe3e1e237e446d7a883b", "ef44a541a8525b7fb671253bdb0bad00",
    "d4d1c6f87c839d87caf2b8bc11f915bc", "6d88a37a110b3efddbf98641ca0093fd",
    "4e54f70e5f5fc9f384a64fb24ea6dc4f", "ead27321b58dbad2312bf5607f8d292f",
    "ac7766f319fadc2128d12941575c006e", "d014f9a8c9ee2589e13f0cc8b6630ca6",
)]
OTHER_BLOCK = bytes.fromhex("00112233445566778899aabbccddeeff")
OTHER_KEY = bytes(range(16))
OTHER_CIPHER = bytes.fromhex("69c4e0d86a7b0430d8cdb78070b4c55a")
ZERO_CIPHER = bytes.fromhex("66e94bd4ef8a2c3b884cfa59ca342b2e")

# Пара: (аргументы функции, ожидаемый ответ). Эти примеры НЕ являются решением.
CASES = {
    "parse_hex_block": [((BLOCK_HEX,), BLOCK), ((" \n" + BLOCK.hex(" ").upper() + "\t",), BLOCK),
                        (("00" * 16,), bytes(16))],
    "bytes_to_state": [((bytes(range(16)),), GRID), ((BLOCK,), START)],
    "state_to_bytes": [((GRID,), bytes(range(16))), ((START,), BLOCK)],
    "add_round_key": [((START, KEY), ADDED), ((ADDED, KEY), START), ((MIXED, KEYS[1]), ROUND_ONE)],
    "sub_bytes": [((ADDED,), SUBBED), (([[0] * 4 for _ in range(4)],), [[0x63] * 4 for _ in range(4)])],
    "shift_rows": [((GRID,), SHIFTED_GRID), ((SUBBED,), SHIFTED)],
    "xtime": [((0,), 0), ((1,), 2), ((0x57,), 0xae), ((0x83,), 0x1d), ((0x80,), 0x1b), ((0xff,), 0xe5)],
    "gf_mul": [((0x57, 0x13), 0xfe), ((0x57, 0x83), 0xc1), ((0xff, 0), 0),
               ((0x83, 1), 0x83), ((0x83, 2), 0x1d), ((0x83, 3), 0x9e)],
    "mix_columns": [((SHIFTED,), MIXED),
                    (([[0xdb]*4, [0x13]*4, [0x53]*4, [0x45]*4],), [[0x8e]*4, [0x4d]*4, [0xa1]*4, [0xbc]*4])],
    "rot_word": [(([0x09, 0xcf, 0x4f, 0x3c],), [0xcf, 0x4f, 0x3c, 0x09]), (([0, 1, 2, 3],), [1, 2, 3, 0])],
    "sub_word": [(([0xcf, 0x4f, 0x3c, 0x09],), [0x8a, 0x84, 0xeb, 0x01]), (([0]*4,), [0x63]*4)],
    "expand_key": [((KEY,), KEYS)],
    "encrypt_block": [((BLOCK, KEY), CIPHER), ((OTHER_BLOCK, OTHER_KEY), OTHER_CIPHER), ((bytes(16), bytes(16)), ZERO_CIPHER)],
    "inv_shift_rows": [((SHIFTED_GRID,), GRID), ((SHIFTED,), SUBBED)],
    "inv_sub_bytes": [((SUBBED,), ADDED), (([[0x63]*4 for _ in range(4)],), [[0]*4 for _ in range(4)])],
    "inv_mix_columns": [((MIXED,), SHIFTED),
                        (([[0x8e]*4, [0x4d]*4, [0xa1]*4, [0xbc]*4],), [[0xdb]*4, [0x13]*4, [0x53]*4, [0x45]*4])],
    "decrypt_block": [((CIPHER, KEY), BLOCK), ((OTHER_CIPHER, OTHER_KEY), OTHER_BLOCK), ((ZERO_CIPHER, bytes(16)), bytes(16))],
}


def describe(value):
    """Показываем байты в Hex, включая матрицы, а не как непонятные escape-коды."""
    if isinstance(value, bytes):
        return value.hex(" ")
    if isinstance(value, list):
        if all(type(item) is int for item in value):
            return " ".join(f"{item:02x}" for item in value)
        return "\n".join(describe(item) for item in value)
    return repr(value)


def same_type(actual, expected):
    if type(actual) is not type(expected):
        return False
    if isinstance(expected, list):
        return len(actual) == len(expected) and all(same_type(a, b) for a, b in zip(actual, expected))
    return True


def reload_student():
    # Импортируем только при нажатии кнопки: даже синтаксическая ошибка
    # в решении ученика не должна мешать запуску учебного приложения.
    aes_student = sys.modules.get("aes_course.student")
    if aes_student is None:
        return importlib.import_module("aes_course.student")
    # Не используем кэш .pyc: ученик может быстро сохранить несколько правок.
    cached = getattr(aes_student, "__cached__", None)
    if cached:
        from pathlib import Path
        Path(cached).unlink(missing_ok=True)
    importlib.invalidate_caches()
    # Обычный reload сохраняет старые имена, удалённые из файла. Новый импорт
    # не позволит случайно проверить вчерашнюю функцию вместо текущего решения.
    sys.modules.pop("aes_course.student", None)
    return importlib.import_module("aes_course.student")


def check_step(name, reload_code=True):
    if name not in CASES:
        return {"status": "error", "text": "", "steps": "Неизвестный шаг."}
    try:
        module = reload_student() if reload_code else importlib.import_module("aes_course.student")
        function = getattr(module, name)
        for number, (arguments, expected) in enumerate(CASES[name], 1):
            inputs = deepcopy(arguments)
            actual = function(*inputs)
            if not same_type(actual, expected) or actual != expected:
                return {"status": "error", "text": "",
                        "steps": f"Пример {number} не совпал.\nВход:\n{describe(list(arguments))}"
                                 f"\nОжидалось ({type(expected).__name__}):\n{describe(expected)}"
                                 f"\nПолучено ({type(actual).__name__}):\n{describe(actual)}"}
            if inputs != arguments:
                return {"status": "error", "text": "", "steps": "Функция изменила входной список. Верните новое значение."}
            # Проверяем отсутствие общих изменяемых строк с входом и друг с другом.
            if isinstance(actual, list) and actual and isinstance(actual[0], list):
                if len({id(row) for row in actual}) != len(actual):
                    raise ValueError("Строки результата должны быть независимыми списками.")
                for arg in inputs:
                    if isinstance(arg, list) and any(row is old for row in actual for old in arg):
                        raise ValueError("Результат использует строки входа. Создайте новые списки строк.")
        if name == "parse_hex_block":
            for invalid in ("", "00"*15, "00"*17, "0"*31, "gg"*16, "0x"+"00"*15):
                try:
                    function(invalid)
                except ValueError:
                    continue
                raise ValueError(f"Неверный ввод {invalid!r} должен вызывать ValueError.")
        return {"status": "passed", "text": "", "steps": "Контрольные примеры пройдены. Можно переходить к следующему шагу."}
    except NotImplementedError as error:
        return {"status": "pending", "text": "", "steps": f"Ещё не реализовано: {error}"}
    except Exception as error:
        # Учебный код может содержать SyntaxError, IndexError и другие ошибки.
        # Показываем их ученику, сохраняя окно приложения работоспособным.
        return {"status": "error", "text": "", "steps": f"{type(error).__name__}: {error}"}


def process_block(text, key, decrypt):
    try:
        module = reload_student()
        block_bytes = module.parse_hex_block(text)
        key_bytes = module.parse_hex_block(key)
        operation = module.decrypt_block if decrypt else module.encrypt_block
        result = operation(block_bytes, key_bytes)
        if type(result) is not bytes or len(result) != 16:
            raise ValueError("Результатом должны быть bytes длины 16.")
        return {"status": "passed", "text": result.hex(" "), "steps": "Блок обработан вашей реализацией. Сверьте его с ожидаемым ответом."}
    except NotImplementedError as error:
        return {"status": "pending", "text": "", "steps": f"Ещё не реализовано: {error}"}
    except Exception as error:
        return {"status": "error", "text": "", "steps": f"{type(error).__name__}: {error}"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("step", nargs="?", choices=list(CASES))
    args = parser.parse_args()
    results = []
    for name in ([args.step] if args.step else [item["id"] for item in LESSONS]):
        result = check_step(name)
        results.append(result["status"])
        print(f"[{result['status']}] {name}: {result['steps']}")
    print(f"Пройдено: {results.count('passed')}; не готово: {results.count('pending')}; ошибок: {results.count('error')}.")
    return 1 if "error" in results else 2 if "pending" in results else 0


if __name__ == "__main__":
    raise SystemExit(main())
