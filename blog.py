import json
from datetime import date


class Post:

    def __init__(self, id: int, author: str, name: str, description: str, tags: list):
        self.id = id
        self.author = author
        self.name = name
        self.description = description
        self.views_count = 0
        self.current_date = date.today()
        self.tags = tags
        # self.img = None

    def __str__(self):
        return f'{self.id}' \
               f'{self.author}' \
               f'{self.name}' \
               f'{self.description}' \
               f'{self.current_date}' \


    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if isinstance(value, int):
            self._id = value
        else:
            raise ValueError('id must be a string')

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if isinstance(value, str) and len(value.strip()) > 2:
            self._author = value
        else:
            raise ValueError('author must be a string')

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and 1 < len(value.strip()) < 40:
            self._name = value
        else:
            raise ValueError('name must be a string')

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if isinstance(value, str) and len(value.strip()) > 1:
            self._description = value
        else:
            raise ValueError('description must be a string')

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, value):
        if isinstance(value, list):
            self._tags = value
        else:
            raise ValueError('tags must be a list')

    def get_short_description(self):
        data = self._description
        if len(data) > 150:
            return data[:148] + ".."
        else:
            return data

    def __dict__(self):
        return {
            'id': self.id,
            'author': self.author,
            'name': self.name,
            'description': self.description,
            'views_count': self.views_count,
            'current date': f'{self.current_date}',
            'tags': self.tags
                }


class Blog:

    def __init__(self, path_file_name):
        self.posts_list = []
        self.path_file_name = path_file_name
        self.load(path_file_name)

    def save(self, path_file_name):
        with open(f"{path_file_name}", "w", encoding="utf-8") as infile:
            json_posts = json.dumps([x.__dict__() for x in self.posts_list])
            infile.write(json_posts)
            infile.close()

    def load(self, path_file_name):
        with open(f"{path_file_name}", "r", encoding="utf-8") as infile:
            dict_of_posts = json.loads(infile.read())
            infile.close()
            self.posts_list = [Post(**x) for x in dict_of_posts]

    def add_post(self, author: str, value_name: str, value_description: str, tags: str) -> object:
        tags = tags.split()
        try:
            post = Post(len(self.posts_list) + 1, author, value_name, value_description, tags)
            self.posts_list.append(post)
        except ValueError:
            print("Ошибка")
            return False
        self.save(self.path_file_name)
        return self.posts_list

    def edit_post(self, value, value_author: str, value_name: str, value_description: str, tags: str) -> list:
        for i in range(0, len(self.posts_list)):
            if self.posts_list[i].id == value:
                self.posts_list[i].name(value_author)
                self.posts_list[i].name(value_name)
                self.posts_list[i].description(value_description)
                self.posts_list[i].current_date = date.today()
                self.posts_list[i].tags(tags.split())
            return self.posts_list[i]
        else:
            ValueError("No such item!")

    def delete_post(self, value):
        for i in range(0, len(self.posts_list)):
            if self.posts_list[i].id == value:
                self.posts_list.pop(i)
            return self.posts_list
        else:
            ValueError("No such item!")

    def get_post(self, value):
        for i in range(0, len(self.posts_list)):
            if self.posts_list[i].id == value:
                return self.posts_list[i]
        else:
            ValueError("No such item!")

    def __del__(self):
        self.save(self.path_file_name)
