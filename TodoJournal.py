""" My awesome todo-manager
"""
import sys
import json

def read_from_file(path_to_file):
    with open(path_to_file) as file_:
        for line in file_.readlines():
            yield line

def main():
    """
    Start of application
    :return: None
    """
    json_file = "../1.json"
    TodoJournal.create(json_file, "test2")

    todo = TodoJournal(json_file)
    #todo.create()
    #json_file = "/not-valid.json"
    for i in range(1, 5):
        todo.add_todo(f"task{i}")

    print(f"Trird elem is {todo[2]}")

    print("Iterating")
    for item in todo:
        print(f"\t{item}")

    print(todo[1:3])

    todo.remove_todo(1)

    print(f"first elem is {todo.first}")
    #todo.first = "my awesome todo"
    print(f"first elem is {todo.first} but real first is is {todo[0]}")
    print(f"last elem is {todo.last}")
    todo.second = "my awesome second"
    print(f"second elem is {todo.second}")
    todo.print()
    # print("File is:")
    # for line in read_from_file(json_file):
    #     print(line, end="")

class TodoJournal:
    """Class with todo"""
    shortcut_names = {"first": 0, "last": -1}

    def __init__(self, path):
        """Init"""
        self.path = path

        self.name = self._parse()["name"]
        self.entries = self._parse()["todos"]

    def __iter__(self):
        print("Gen started")
        for entry in self.entries:
            print("New iteration")
            yield entry
        print("Gen ended")
        #return iter(self.entries)

    def __getitem__(self, index):
        return self.entries[index]

    @staticmethod
    def create(filename, name):
        with open(filename, "w", encoding='utf-8') as todo_file:
            json.dump(
                {"name": name, "todos": []},
                todo_file,
                sort_keys=True,
                indent=4,
                ensure_ascii=False,
            )

    def add_todo(self, new_todo):
        """Adding new todo to todo-file
        todo - text of todo to add"""
        data = self._parse()

        name = data["name"]
        todos = data["todos"]

        todos.append(new_todo)
        self.entries.append(new_todo)

        new_data = {
            "name": name,
            "todos": todos,
        }

        self._update(new_data)

    def remove_todo(self, index):
        """Removing todo by its index
        index - number of todo to delete, starting with 0"""
        data = self._parse()
        name = data["name"]
        todos = data["todos"]

        todos.remove(todos[index])

        new_data = {
            "name": name,
            "todos": todos,
        }

        self._update(new_data)

    def _update(self, new_data):
        with open(self.path, "w", encoding='utf-8') as todo_file:
            json.dump(
                new_data,
                todo_file,
                sort_keys=True,
                indent=4,
                ensure_ascii=False,
            )

    def _parse(self):
        """Reading from self.path and returning json with todos
        :returns json with todos
        """
        try:
            with open(self.path, 'r') as todo_file:
                data = json.load(todo_file)
            return data
        except FileNotFoundError as err:
            print(f"{err}")
            # или свое исключение
            print(f"Не существует такой тудушки: {self.path}")
            sys.exit(1)

    def print(self):
        """
        Print todo in console
        ---------------------
        Returns: None
        """
        out = '=' * 10 + self.name + '=' * 10 + '\n'
        for i in range(len(self.entries)):
            out += f"{i + 1}: {self.entries[i]}\n"
        out += '=' * (20+len(self.name))
        print(out)

    def __getattr__(self, item):
        index = self.shortcut_names.get(item, None)
        if index is not None:
            return self.entries[index]

        raise AttributeError(f"{type(self).__name__} object has no attribute {item}")

    def __setattr__(self, name, value):
        if name in self.shortcut_names:
            error_msg = f"readonly attribute {name}"
            raise AttributeError(error_msg)
        super().__setattr__(name, value)  # по умолчанию вызываем обычный setattr из супер класса


if __name__ == '__main__':
    main()
