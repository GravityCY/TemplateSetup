# Get program args
import json
import os
from pathlib import Path
import re

project_path: Path
resources_path: Path
java_path: Path
mod_id: str
mod_class_name: str
mod_package_name: str
mod_name: str
mod_version: str
mod_description: str
mod_author: str
new_package_qualifier: str


def rename_file(path: Path, old_name: str, new_name: str):
    try:
        os.rename(path.joinpath(old_name), path.joinpath(new_name))
        return True
    except FileNotFoundError:
        return False


def replace_file_contents(file_path: Path, search_string: str, new_string):
    file_contents: str
    with open(file_path, "r") as file:
        file_contents = file.read()
    file_contents = re.sub(search_string, new_string, file_contents)
    with open(file_path, "w") as file:
        file.write(file_contents)


def replace_json(path: Path, key: str, value: str):
    data: json
    with open(path, "r") as file:
        data = json.load(file)

    data[key] = value

    with open(path, "w") as json_file:
        json.dump(data, json_file, indent=4)


def replace_json_all(path: Path, key_values: dict):
    data = from_json_file(path)
    for key, value in key_values.items():
        data[key] = value
    write_json_file(path, data)


def from_json_file(path: Path):
    with open(path, "r") as json_file:
        return json.load(json_file)


def write_json_file(path: Path, data):
    with open(path, "w") as file:
        json.dump(data, file, indent=4)


def main():
    global project_path, mod_id, mod_name, \
        mod_version, mod_description, mod_author, \
        mod_package_name, mod_class_name, resources_path, \
        java_path, new_package_qualifier

    project_path = Path(input("Enter Project Path: "))
    mod_id = input("Enter Mod ID: ")
    mod_class_name = input("Enter Mod Class Name: ")
    mod_package_name = input("Enter Mod Package Name: ")
    mod_name = input("Enter Mod Name: ")
    mod_version = input("Enter Mod Version: ")
    mod_description = input("Enter Mod Description: ")
    mod_author = input("Enter Mod Author: ")

    if mod_id == "":
        mod_id = "example"
    if mod_package_name == "":
        mod_package_name = "example"
    if mod_name == "":
        mod_name = "Example"
    if mod_version == "":
        mod_version = "0.1.0+1.19.4"
    if mod_description == "":
        mod_description = "Example Mod"
    if mod_author == "":
        mod_author = "GravityIO"

    resources_path = project_path.joinpath("src/main/resources")
    java_path = project_path.joinpath("src/main/java")
    new_package_qualifier = f"me.gravityio.{mod_package_name}"

    format_gradle_properties()
    format_src()
    format_res()


def format_res():
    format_fabric_json()
    format_mixins_json()
    rename_file(resources_path.joinpath("assets"), "example", mod_id)


def format_mixins_json():
    mixins_json_path = resources_path.joinpath("example.mixins.json")
    mixins_json = from_json_file(mixins_json_path)
    mixins_json["package"] = f"{new_package_qualifier}.mixins.impl"
    write_json_file(mixins_json_path, mixins_json)

    rename_file(resources_path, "example.mixins.json", f"{mod_id}.mixins.json")


def format_fabric_json():
    fabric_mod_path = resources_path.joinpath("fabric.mod.json")
    fabric_json = from_json_file(fabric_mod_path)
    fabric_json["entrypoints"]["main"] = [f"me.gravityio.{mod_package_name}.{mod_class_name}"]
    fabric_json["mixins"] = [f"{mod_id}.mixins.json"]
    write_json_file(fabric_mod_path, fabric_json)


def format_src():
    package_path = java_path.joinpath("me/gravityio/example")
    main_class_path = package_path.joinpath("ExampleMod.java")
    mixin_class_path = package_path.joinpath(f"mixins/impl/ExampleMixin.java")

    replace_file_contents(main_class_path, r"package me\.gravityio\..+;", f"package me.gravityio.{mod_package_name};")
    replace_file_contents(main_class_path, r"public class \w+", f"public class {mod_class_name}")
    replace_file_contents(main_class_path, r"MOD_ID = .+", f"MOD_ID = \"{mod_id}\";")
    replace_file_contents(mixin_class_path, r"package me\.gravityio\..+;",
                          f"package me.gravityio.{mod_package_name}.mixins.impl;")

    rename_file(package_path, "ExampleMod.java", f"{mod_class_name}.java")
    rename_file(java_path.joinpath("me/gravityio"), "example", mod_package_name)


def format_gradle_properties():
    path = project_path.joinpath("gradle.properties")
    mod_id_search = r"mod_id = .+"
    mod_id_replacement = f"mod_id = {mod_id}"

    mod_name_search = r"mod_name = .+"
    mod_name_replacement = f"mod_name = {mod_name}"

    mod_version_search = r"mod_version = .+"
    mod_version_replacement = f"mod_version = {mod_version}"

    mod_description_search = r"mod_description = .+"
    mod_description_replacement = f"mod_description = {mod_description}"

    mod_author_search = r"mod_author = .+"
    mod_author_replacement = f"mod_author = {mod_author}"

    replace_file_contents(path, mod_id_search, mod_id_replacement)
    replace_file_contents(path, mod_name_search, mod_name_replacement)
    replace_file_contents(path, mod_version_search, mod_version_replacement)
    replace_file_contents(path, mod_description_search, mod_description_replacement)
    replace_file_contents(path, mod_author_search, mod_author_replacement)


main()
