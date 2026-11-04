"""Проверки учебной обвязки. Решения AES здесь нет.

Эти тесты остаются рабочими, когда ученик начинает заполнять функции.
Сами решения проверяются отдельно командой python -m aes_course.checks.
"""

import unittest
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from aes_course.constants import S_BOX, INV_S_BOX
from aes_course.lessons import LESSONS, guide_text
from aes_course.checks import CASES, check_step, process_block, BLOCK_HEX, KEY_HEX, CIPHER
from backend import Backend


class AesScaffoldTests(unittest.TestCase):
    def test_tables_are_inverse_permutations(self):
        self.assertEqual(sorted(S_BOX), list(range(256)))
        self.assertEqual(sorted(INV_S_BOX), list(range(256)))
        self.assertTrue(all(INV_S_BOX[S_BOX[x]] == x for x in range(256)))

    def test_guide_and_lessons_stay_in_sync(self):
        self.assertEqual([item["id"] for item in LESSONS], list(CASES))
        path = Path(__file__).resolve().parents[1] / "aes_course" / "WORKBOOK.md"
        self.assertEqual(path.read_text(encoding="utf-8"), guide_text())

    def test_pending_is_distinct_from_failure(self):
        module = SimpleNamespace(xtime=Mock(side_effect=NotImplementedError("xtime")))
        with patch("aes_course.checks.reload_student", return_value=module):
            self.assertEqual(check_step("xtime")["status"], "pending")
        with patch("aes_course.checks.reload_student", side_effect=SyntaxError("line 7")):
            result = check_step("xtime")
            self.assertEqual(result["status"], "error")
            self.assertIn("SyntaxError", result["steps"])

    def test_correct_and_wrong_answers(self):
        expected = [answer for _, answer in CASES["xtime"]]
        with patch("aes_course.checks.reload_student", return_value=SimpleNamespace(xtime=Mock(side_effect=expected))):
            self.assertEqual(check_step("xtime")["status"], "passed")
        for answer in (None, -1, False):
            with patch("aes_course.checks.reload_student", return_value=SimpleNamespace(xtime=Mock(return_value=answer))):
                result = check_step("xtime")
                self.assertEqual(result["status"], "error")
                self.assertIn("Ожидалось", result["steps"])

    def test_input_mutation_is_reported(self):
        def mutating(state):
            state[0][0] = 999
            return deepcopy(CASES["shift_rows"][0][1])
        with patch("aes_course.checks.reload_student", return_value=SimpleNamespace(shift_rows=mutating)):
            self.assertIn("изменила", check_step("shift_rows")["steps"])

    def test_parser_must_reject_bad_input(self):
        answers = [answer for _, answer in CASES["parse_hex_block"]]
        # Мок возвращает контрольные ответы, затем ошибочно принимает пустой ввод.
        module = SimpleNamespace(parse_hex_block=Mock(side_effect=answers + [b""]))
        with patch("aes_course.checks.reload_student", return_value=module):
            self.assertEqual(check_step("parse_hex_block")["status"], "error")

    def test_backend_keeps_result_empty_on_incomplete_or_broken_solution(self):
        for error, status in ((NotImplementedError("parse_hex_block"), "pending"),
                              (ValueError("wrong length"), "error"), (SyntaxError("bad code"), "error")):
            with patch("aes_course.checks.reload_student", side_effect=error):
                answer = Backend().process_aes(BLOCK_HEX, KEY_HEX, False)
                self.assertEqual(answer["status"], status)
                self.assertEqual(answer["text"], "")

    def test_block_result_contract(self):
        module = SimpleNamespace(parse_hex_block=Mock(return_value=bytes(16)),
                                 encrypt_block=Mock(return_value=CIPHER))
        with patch("aes_course.checks.reload_student", return_value=module):
            self.assertEqual(process_block(BLOCK_HEX, KEY_HEX, False)["text"], CIPHER.hex(" "))
            module.encrypt_block.return_value = b"short"
            self.assertEqual(process_block(BLOCK_HEX, KEY_HEX, False)["status"], "error")


if __name__ == "__main__":
    unittest.main()
