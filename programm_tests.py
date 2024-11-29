import unittest
from unittest.mock import patch, mock_open
import re
import requests

from lab2 import is_strong_password, find_passwords_in_url, find_passwords_in_file

class TestPasswordChecker(unittest.TestCase):
    
    def test_is_strong_password_valid(self):
        """Тест на проверку сильного пароля"""
        self.assertTrue(is_strong_password("Valid1@Password"))
        
    def test_is_strong_password_invalid_no_upper(self):
        """Тест на проверку пароля без заглавной буквы"""
        self.assertFalse(is_strong_password("invalid1@password"))
        
    def test_is_strong_password_invalid_no_digit(self):
        """Тест на проверку пароля без цифры"""
        self.assertFalse(is_strong_password("Invalid@Password"))
        
    def test_is_strong_password_invalid_no_special_char(self):
        """Тест на проверку пароля без спецсимвола"""
        self.assertFalse(is_strong_password("Invalid1234"))
    
    def test_is_strong_password_invalid_too_short(self):
        """Тест на проверку слишком короткого пароля"""
        self.assertFalse(is_strong_password("Sh1!"))
        
    @patch("requests.get")
    def test_find_passwords_in_url_success(self, mock_get):
        """Тест на нахождение паролей на веб-странице"""
        # Подготовим mock-ответ от requests
        mock_get.return_value.text = """
        Here are some passwords: Strong1@password, weakpass, Another1$password.
        """
        url = "http://example.com"
        result = find_passwords_in_url(url)
        self.assertEqual(result, ["Strong1@password", "Another1$password"])
    
    @patch("requests.get")
    def test_find_passwords_in_url_error(self, mock_get):
        """Тест на ошибку при запросе к URL"""
        mock_get.side_effect = requests.exceptions.RequestException("Request failed")
        url = "http://example.com"
        result = find_passwords_in_url(url)
        self.assertEqual(result, [])
        
    @patch("builtins.open", new_callable=mock_open, read_data="Here are some passwords: Strong1@password, weakpass, Another1$password.")
    def test_find_passwords_in_file(self, mock_file):
        """Тест на нахождение паролей в файле"""
        file_path = "passwords.txt"
        result = find_passwords_in_file(file_path)
        self.assertEqual(result, ["Strong1@password", "Another1$password"])
        
    @patch("builtins.open", new_callable=mock_open, read_data="Here are some passwords: weakpass.")
    def test_find_passwords_in_file_no_strong_passwords(self, mock_file):
        """Тест на отсутствие сильных паролей в файле"""
        file_path = "passwords.txt"
        result = find_passwords_in_file(file_path)
        self.assertEqual(result, [])
    
    @patch("builtins.open", new_callable=mock_open)
    def test_find_passwords_in_file_error(self, mock_file):
        """Тест на ошибку при чтении файла"""
        mock_file.side_effect = IOError("File not found")
        file_path = "non_existent_file.txt"
        result = find_passwords_in_file(file_path)
        self.assertEqual(result, [])

# if __name__ == "__main__":
#     unittest.main()
