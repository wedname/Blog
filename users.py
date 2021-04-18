import json
import re


class User:

    def __init__(self, name: str, email: str, password: str):
        self.id = None
        self.name = name
        self.email = email
        self.telephone = None
        self.password = password
        # self.avatar = None

    regular_email = r'(^|\s)[-a-z0-9_.]+@([-a-z0-9]+\.)+[a-z]{2,6}(\s|$)'
    email_regex = re.compile(regular_email)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and len(value.split()) < 3:
            self._name = value
        else:
            raise ValueError('name должен быть типом данных str и записан в формате Фамилия Имя Отчество.')

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value, email_regex=email_regex):
        if isinstance(value, str) and email_regex.findall(value):
            self._email = value
        else:
            raise ValueError('В почте нет символов "@" и "." или email это не строка')

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        if isinstance(value, str):
            has_upper = False
            has_lower = False
            has_digit = False
            has_spec_char = False
            if not len(value) > 8:
                raise ValueError("Пароль должен быть > 8 символов!")
            for char in value:
                if char.isupper():
                    has_upper = True
                if char.islower():
                    has_lower = True
                if char.isdigit():
                    has_digit = True
                if not char.isalnum():
                    has_spec_char = True
            if not has_upper:
                raise ValueError("В пароле должна быть минимум 1 большая буква!")
            if not has_lower:
                raise ValueError("В пароле должна быть минимум 1 маленькая буква!")
            if not has_digit:
                raise ValueError("В пароле должна быть минимум 1 цифра!")
            if not has_spec_char:
                raise ValueError("В пароле должен быть минимум 1 спецсимвол!")
            self._password = value
        else:
            raise ValueError('password не строка')

    def __dict__(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'telephone': self.telephone,
            'password': self.password
                }


class Users:

    def __init__(self, path_file_name):
        self.users = []
        self.path_file_name = path_file_name
        self.load(path_file_name)

    def __del__(self):
        self.save(self.path_file_name)

    def save(self, path_file_name):
        with open(f"{path_file_name}", "w", encoding="utf-8") as infile:
            infile.write(json.dumps([dict(x) for x in self.users]))
            infile.close()

    def load(self, path_file_name):
        with open(f"{path_file_name}", "r", encoding="utf-8") as infile:
            self.users = json.loads(infile.read())
            infile.close()

    def create_user(self, name, email, password):
        try:
            user = User(name, email, password)
            user.id = len(self.users) + 1
        except ValueError as e:
            print(e)
            return False
        if self.search_user(email) is None:
            self.users.append({
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'telephone': user.telephone,
                'password': user.password
            })
            self.save(self.path_file_name)
            return True
        else:
            print("Пользователь с таким email уже есть!")
            return False

    def search_user(self, user_email):
        for i in range(len(self.users)):
            if user_email == self.users[i]['email']:
                return i
        return None

    def search_user_id(self, user_id):
        for i in range(len(self.users)):
            if user_id == self.users[i]['id']:
                return i
        return None

    def auth_user_id(self, email):
        for i in range(len(self.users)):
            if email == self.users[i]['email']:
                return self.users[i]['id']
        return None

    def edit_user(self, search_id, name, email, password):
        user_id = self.search_user_id(search_id)
        if user_id is None:
            return False
        user = self.users[user_id]
        user.name = name
        user.email = email
        user.password = password
        return True

    def delete_user(self, search_id):
        user = self.search_user_id(search_id)
        if user is None:
            return False
        self.users.pop(user)
        return True

