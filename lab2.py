import re
import requests

strong_password = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$"

def is_strong_password(password):     # проверяем пароль, введенный пользователем, на соответствие образцу
    return bool(re.match(strong_password, password))

def find_passwords_in_url(url):
    try:
        response = requests.get(url) # отпрапвляем http-запрос
        text = response.text
        potential_passwords = re.findall(r'\b[A-Za-z\d!@#$%^&*]{8,}\b', text)
        strong_passwords = [password for password in potential_passwords if is_strong_password(password)]
        return strong_passwords  #возвращает список сильных паролей, которые были найдены на странице.
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к URL: {e}")
        return []

def find_passwords_in_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            print("Содержимое файла в сыром виде:", repr(text))  # Сырой вывод содержимого
            potential_passwords = re.findall(r'\b[A-Za-z\d!@#$%^&*()_+=\-{}|:"<>?~`.,;\'\[\]\\\/]{8,}\b', text)
            print("Потенциальные пароли:", potential_passwords)  # Потенциальные пароли
            strong_passwords = [password for password in potential_passwords if is_strong_password(password)]
            print("Сильные пароли:", strong_passwords)  # Сильные пароли
            return strong_passwords
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return []

print(is_strong_password("Str0ngP@ssw0rd"))  # True
print(is_strong_password("weakpassword"))   # False
#print(find_passwords_in_url("http://localhost:8000/example_passwords.html"))
print(find_passwords_in_file("C:/Users/Alice/Desktop/лаба2/пароли.txt"))


