import json
from pathlib import Path


class Template:

    def __init__(self, name, path):
        self.keys: dict[str, dict] = {}
        self.replacements: dict[str, str] = {}
        self.name: str = name
        self.path: Path = path

    def load(self):
        with open(self.path.joinpath("setup.template.json"), "r") as file:
            self.keys = json.load(file)["keys"]  # type: dict[str, dict]

    def collect_keys(self):
        return self.keys.keys()

    def collect_content(self):
        temp: dict[str, list[str]] = {}
        for key, value in self.keys.items():
            temp[key] = value["content"]
        return temp

    # a/b/@{c}
    # a/b/@{c}/@{d}
    def collect_files(self):
        temp: list[Replacement] = self.__get_all_replacements()
        temp.sort(key=sort_replacement)
        return temp

    def __get_all_replacements(self):
        out: list[Replacement] = list()

        for replacement_key, replacement_object in self.keys.items():
            if "file" not in replacement_object:
                continue

            for replacement_path in replacement_object["file"]:
                out.append(Replacement(replacement_key, replacement_path))

        return out

    def set_replacement(self, key: str, value: str):
        if key not in self.keys:
            pass

        self.replacements[key] = value

    def get_replacement(self, key):
        return self.replacements[key]

    def __str__(self):
        return f"{self.name}: {self.path}"


class Replacement:
    def __init__(self, key: str, path: str):
        self.key: str = key
        self.path: str = path


def sort_replacement(replacement: Replacement):
    return 0 - replacement.path.count("/")
