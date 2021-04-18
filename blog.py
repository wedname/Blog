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
        if isinstance(value, str):
            self._name = value
        else:
            raise ValueError('name must be a string')

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if isinstance(value, str):
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


class Blog:

    def __init__(self):
        self.posts_list = []

    def add_post(self, author: str, value_name: str, value_description: str, tags: str) -> object:
        tags = tags.split()
        return self.posts_list.append(Post(len(self.posts_list)+1, author, value_name, value_description, tags))

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
