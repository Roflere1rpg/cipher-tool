"""Проверки обратимости и ошибок ввода: python -m unittest discover -s tests."""

import unittest
from math import gcd

from backend import Backend
from ciphers import ENGLISH, RUSSIAN, affine, atbash, caesar, vigenere, xor_cipher


class CipherTests(unittest.TestCase):
    def test_known_examples(self):
        self.assertEqual(caesar("ABC XYZ", 3, ENGLISH), "DEF ABC")
        self.assertEqual(atbash("ABC", ENGLISH), "ZYX")
        self.assertEqual(vigenere("ATTACKATDAWN", "LEMON", ENGLISH), "LXFOPVEFRNHR")
        self.assertEqual(affine("ABC", 5, 8, ENGLISH), "INS")
        self.assertEqual(xor_cipher("ABC", "key"), "2a 27 3a")

    def test_alphabet_cipher_round_trips(self):
        for alphabet, key in ((ENGLISH, "KEY"), (RUSSIAN, "КЛЮЧ")):
            text = alphabet + alphabet.upper() + " 123!?\n😀"
            for shift in range(-70, 71):
                self.assertEqual(caesar(caesar(text, shift, alphabet), -shift, alphabet), text)
            self.assertEqual(atbash(atbash(text, alphabet), alphabet), text)
            self.assertEqual(vigenere(vigenere(text, key, alphabet), key, alphabet, True), text)
            for a in range(1, len(alphabet)):
                for b in range(len(alphabet)):
                    if gcd(a, len(alphabet)) == 1:
                        self.assertEqual(affine(affine(text, a, b, alphabet), a, b, alphabet, True), text)
                    else:
                        for decrypt in (False, True):
                            with self.assertRaises(ValueError):
                                affine(text, a, b, alphabet, decrypt)

    def test_xor_preserves_exact_text(self):
        for text in ("", "Hello, world!", "Привет, мир!", " a  b\n\t😀\0"):
            for key in ("secret", "ключ", "😀"):
                with self.subTest(text=text, key=key):
                    self.assertEqual(xor_cipher(xor_cipher(text, key), key, True), text)

    def test_vigenere_rejects_invalid_keys(self):
        for alphabet, keys in ((ENGLISH, ("", "ключ", "KEЯ", "K1", "A B")),
                               (RUSSIAN, ("", "KEY", "КЛЮЧK"))):
            for key in keys:
                for decrypt in (False, True):
                    with self.assertRaises(ValueError):
                        vigenere("ABC Привет", key, alphabet, decrypt)

    def test_backend_reports_errors_without_result(self):
        backend = Backend()
        for decrypt in (False, True):
            for answer in (
                backend.process_vigenere("Привет", "KEY", "Русский", decrypt),
                backend.process_vigenere("ABC", "", "Английский", decrypt),
                backend.process_affine("AN", 2, 0, "Английский", decrypt),
                backend.process_affine("аб", 11, 0, "Русский", decrypt),
                backend.process_xor("ABC", "", decrypt),
            ):
                self.assertEqual(answer["text"], "")
                self.assertTrue(answer["steps"].startswith("Ошибка:"))
        # Огромное число, неверные символы и суррогат не должны выходить
        # необработанным исключением в интерфейс Qt.
        for value in ("zz", "110000", "f" * 100, "-1", "0x41", "d861"):
            answer = backend.process_xor(value, "a", True)
            self.assertEqual(answer["text"], "")
            self.assertTrue(answer["steps"].startswith("Ошибка:"))


if __name__ == "__main__":
    unittest.main()
