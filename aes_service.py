"""Данные для страницы AES: результат, состояния каждого шага и ключи раундов."""

from aes_cipher import parse_hex_block, encrypt_block, decrypt_block, state_to_bytes, bytes_to_state

DESCRIPTIONS = {
    "Input": "Входные байты расположены в матрице 4 × 4 по столбцам. Это начальное состояние.",
    "KeyExpansion": (
        "K0 совпадает с введённым ключом. Каждый следующий ключ получается из предыдущего "
        "с помощью поворота, замены байтов, раундовой константы и XOR. "
        "На этом шаге мы готовим ключи, поэтому матрица данных остаётся прежней. "
        "Все 11 ключей показаны ниже."
    ),
    "SubBytes": "Каждый байт заменён значением из таблицы S-box. Положение клеток сохранено.",
    "ShiftRows": "Строки 0, 1, 2 и 3 циклически сдвинуты влево на 0, 1, 2 и 3 позиции.",
    "MixColumns": (
        "Каждый новый байт вычислен из четырёх исходных байтов своего столбца. "
        "Расчёт первого столбца из «Примера» разобран во вкладке «Теория»."
    ),
    "AddRoundKey": "К каждой клетке применён XOR с соответствующим байтом раундового ключа.",
    "InvShiftRows": "Строки 0, 1, 2 и 3 циклически сдвинуты вправо на 0, 1, 2 и 3 позиции.",
    "InvSubBytes": "Значения байтов восстановлены с помощью обратной таблицы S-box.",
    "InvMixColumns": "Выполнено обратное смешивание байтов каждого столбца.",
}


def _cells(state):
    # QML рисует клетки строками; сериализация блока выполняется по столбцам.
    return [f"{value:02x}" for row in state for value in row]


def process_aes(text, key, decrypt):
    try:
        try:
            block = parse_hex_block(text)
        except ValueError as error:
            raise ValueError(f"Входной блок: {error}") from error
        try:
            key_bytes = parse_hex_block(key)
        except ValueError as error:
            raise ValueError(f"Ключ: {error}") from error
        raw_trace = []
        result = (decrypt_block if decrypt else encrypt_block)(block, key_bytes, raw_trace)
        keys = next(item["keys"] for item in raw_trace if item["operation"] == "KeyExpansion")
        steps = []
        previous = raw_trace[0]["state"]
        for number, event in enumerate(raw_trace):
            state = event["state"]
            operation = event["operation"]
            key_index = event["keyIndex"]
            prefix = "Подготовка" if event["round"] == 0 else f"Раунд {event['round']}"
            key_label = f"K{key_index}" if key_index is not None else ""
            description = DESCRIPTIONS[operation]
            if event["round"] == 10:
                description += " Это заключительный раунд; смешивания столбцов в нём нет."
            steps.append({
                "title": f"{number+1}. {prefix} · {operation}" + (f" · {key_label}" if key_label else ""),
                "operation": operation, "round": event["round"], "description": description,
                "before": _cells(previous), "after": _cells(state),
                "beforeHex": state_to_bytes(previous).hex(" "),
                "afterHex": state_to_bytes(state).hex(" "),
                "keyLabel": key_label,
                "keyHex": keys[key_index].hex(" ") if key_index is not None else "",
                "keyCells": _cells(bytes_to_state(keys[key_index])) if key_index is not None else [],
            })
            previous = state
        return {"status": "ok", "text": result.hex(" "), "steps": steps,
                "roundKeys": [{"label": f"K{i}", "hex": value.hex(" ")} for i, value in enumerate(keys)],
                "message": "Расшифровка завершена." if decrypt else "Шифрование завершено."}
    except ValueError as error:
        # При ошибке не оставляем на странице состояния от предыдущего ввода.
        return {"status": "error", "text": "", "steps": [], "roundKeys": [], "message": str(error)}
