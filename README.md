# TemplateSetup
A small python utility, that copies a 'template' folder
to an output path that has replaceable strings that the 
user can replace through the command line.

## How To

You essentially create a folder in `./templates` named whatever you
want, you put a file in the folder you just made named `setup.template.json`, this will contain the keys
that the user can replace, the paths, and what type of `replacement` it is, there's 2 replacement types.


### File

When you specify a file key, it replaces the file name of the path you give it with 
the template string with the users input

Example:
```json
{
    "keys": {
        "filename": {
            "file": [
              "@{filename}.json"
            ]
        }   
    }
}
```
The above will replace the the file at `@{filename}.json` with whatever the user enters.

```
0: [Enter "filename": 'helloworld']
1: [Rename Path '@{filename}.json' -> 'helloworld.json']
```

### Content
When you specify a content key, it will replace any of the contents of a given file, that has the key @{name_of_the_key}
with whatever the user inputs

Here's an simple example, in a file called `example.md`

**./example.md**
```markdown
# Welcome to @{name}!
This would be an example using the content key type,
to replace the name of some cool string like @{name}! 
```

And an example of what the `setup.template.json` would look like
```json
{
  "keys": {
    "name": {
      "content": [
        "example.md"
      ]
    }
  }
}
```
The above will replace anything marked as @{name} 
in example.md with whatever the user enters
```
0: [Enter "content": 'Some Cool Name']
1: [Replace all '@{name}' in 'readme.md' -> 'Some Cool Name']
```

---

Optionally you can put a `on_open` key in in the root of the `setup.template.json`;
```json
{
  "keys": ...,
  "on_open": {
    "run_console": "echo ${out_folder}"
  }
}
```
Right now the only available action to take `on_open` is
to run something in the console, can take 1 variable 
currently which is hardcoded;

* `out_folder` would become `"./some_folder/that_user_specified"` (adds quotation marks)