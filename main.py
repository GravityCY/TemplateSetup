import os
import shutil
import re

from api.Template import Template
from pathlib import Path
import globals

templates = {}
current_template: Template
cwd_path = Path(os.getcwd())
templates_path = Path(cwd_path.joinpath("templates"))
output_path = Path("test")
isDev = False
cache = {}


def debug(message, *args, **kwargs):
    if not isDev:
        return
    print(message, *args, **kwargs)


def load_templates():
    for path in os.listdir(templates_path):
        template_path = Path(templates_path.joinpath(path))
        if not template_path.joinpath("setup.template.json").is_file():
            continue
        debug(f"Adding template of name {template_path.name} at path {template_path}")
        templates[template_path.name] = template_path


def get_templates_as_list():
    out: list[Template] = list()
    for name, path in templates.items():
        temp = Template(name, path)
        out.append(temp)
    return out


def replace_file_content(path: Path, search: str, replacement: str):
    with open(path, "r") as file:
        data = file.read()
    data = re.sub(search, replacement, data)
    with open(path, "w") as file:
        file.write(data)


# Rename a part of the name of a file
def rename_file(path: Path, search: str, replacement: str):
    try:
        directory = path.parent
        new_file_name = re.sub(search, replacement, path.name)
        new_file_path = directory.joinpath(new_file_name)
        os.rename(path, new_file_path)
        return new_file_name
    except FileNotFoundError:
        return None


def replace_content(template: Template, out_path: Path):
    for key, paths in template.collect_content().items():
        for path_string in paths:
            path = out_path.joinpath(path_string)
            search = globals.DEFAULT_FORMAT % key
            replacement = template.get_replacement(key)
            replace_file_content(path, search, replacement)


def get_renamed_path(path: Path):
    out: str = ""

    for parent in path.parents:
        if parent.name in cache:
            return cache[parent.name]
        else:
            cache[parent.name] = parent

    return out


def replace_files(template: Template, out_path: Path):
    pass
    for replacement in template.collect_files():
        path = out_path.joinpath(replacement.path)
        search = globals.DEFAULT_FORMAT % replacement.key
        replacement = template.get_replacement(replacement.key)
        rename_file(path, search, replacement)


def ignore_setup_template(directory: str, filenames: list[str]):
    directory_path = Path(directory)
    return ["setup.template.json"] if current_template.path == directory_path else []


def main():
    global current_template, output_path

    load_templates()
    print("Available Templates: ")
    templates_list = get_templates_as_list()
    for index, template in enumerate(templates_list):
        print(f" [{index}] {template.name}: {template.path}")
    template_index = int(input("Choose a Template: "))
    print(f"Selected: ({templates_list[template_index]})")
    output_path = Path(input("Enter output path: ")).resolve()
    current_template = templates_list[template_index]
    current_template.load()
    shutil.copytree(current_template.path, output_path, ignore=ignore_setup_template)
    print(f"Copied {current_template.name} from {current_template.path} to {output_path}")
    for key in current_template.collect_keys():
        current_template.set_replacement(key, input(f"Enter {key}: "))

    replace_content(current_template, output_path)
    replace_files(current_template, output_path)


main()
