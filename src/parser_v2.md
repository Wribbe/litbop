# Literate source for extended bootstrapped parser.

### Additions - Todo:
* [ ] - Support `<<path_file, 'a'>>` syntax for appending to existing files.
* [ ] - Support dynamic variables with `<<{{ignore_file}}, 'w'>>` syntax.
* [ ] - If multiple `<<tag>>=`, the last one should take precedence.
* [ ] - Figure out why 2x escapes are needed `\\\\s`, optimally no
        escapes needed, `\s`.

### Defining the main structure of the lib.

```python
<<./litbop/liblitbop.py>>=
<<imports>>
<<global definitions>>
<<helper methods>>
def parse(data):
  <<regexes>>
  <<find tags and scopes>>
  <<consolidate tags>>
#  <<resolve nested tags>>
  <<parse and process tags>>
  <<write data to disk>>
@
```

Make sure there is a `__init__.py` file in the `litbop` directory.

```python
<<./litbop/__init__.py>>=
# File needed to make litbop a module.
@
```

### First batch of regular expressions.

Continue using `re` module to find tags and scope.

```python
<<imports>>=
import re
@
```

Define globals that will be used for parsing.

```python
<<global definitions>>=
START_TAG = "<<"
END_TAG = ">>"
END_SCOPE = "@"
@
```

Use the globals to define the regular expressions.

```python
<<regexes>>=
re_tag_usage = f"{START_TAG}.*?{END_TAG}"
re_tag_scope = f"^({re_tag_usage})[+=]\\s*(.*?)\\s*^{END_SCOPE}"
@
```

A valid match of a scope includes the following:
1. Capturing the `<<tag_name>>` without additional characters.
1. Capturing the scope after definitions or additions.
    * Captured scope should not include any whitespace trailing after the definition.
    * Captured scope should only end when encountering `@` at the start of its
      own line, and the `@` should not be included in the returned scope.
    * Any whitespace between the last scope line and `@` should not be
      captured.

Deconstruction of `re_tag_scope`:

1. Since the match for additional chars `[+=]` is outside of the capture group,
   `(` and `)` the tag will be captured without additional characters.
1. Second capture group between the tag and `@` captures any defined scope.
    * First whitespace match `\s*` after tag definition outside of capture group.
    * Using `^` in combination with `re.MULTILINE` specifies that the preceding
      character to `@` should be a newline in order for `^@` to match.
    * Second whitespace match `\s*` between scope and `@` discards any trailing
      whitespace.

### Envisioning the end-result.

When everything is said and done, the final operation of writing data to disk
should involve no additional poking.

```python
<<write data to disk>>=
for tag in list_actionable_tags:
  process_tag(tag)
@
```

Which needs the method `process_tag` and a list of tags named
`list_actionable_tags`.

```python
<<helper methods>>=
<<helper_process_tag>>
@
```

The actionable list should be available after the `<<parse and process tags>>`
section.

```python
<<parse and process tags>>=
list_actionable_tags = []
@
```

Define the stub for the first helper method, to be resolved later:

```python
<<helper_process_tag>>=
def process_tag(tag):
  pass
#  <<identify tag type>>
#  <<proceed with doing the correct thing>>
@
```

### Getting the first list of tags and scopes.

Use `re_tag_scope` to find all the available tags, use `re.DOTALL` in order to
make `.` match newlines, and `re.MULTILINE` in order to make `^` and `$` work
as expected in a multi line context.

```python
<<find tags and scopes>>=
list_tags_and_scopes = re.findall(re_tag_scope, data, re.DOTALL+re.MULTILINE)
@
```

### Consolidating tags into one scope.

Apply previous method of appending scopes to an empty list in a
dictionary keyed with all available tag definitions. Sort out all unique keys
in `list_tags_and_scopes` by using a `set` and then create a dictionary with
empty lists, keyed on each unique tag using `dictionary-comprehension`.

```python
<<consolidate tags>>=
tags_unique = set([key for key,_ in list_tags_and_scopes])
dict_consolidated_scopes = {tag:[] for tag in tags_unique}
@
```

Iterate over all the tags and data in `list_tags_and_scopes` and add them to
`dict_consolidated_scopes`.

```python
<<consolidate tags>>+
for tag, data_scope in list_tags_and_scopes:
  dict_consolidated_scopes[tag].append(data_scope)
@
```

Use `os.linesep.join()` to concatenate the appended parts into a single string.

```python
<<consolidate tags>>+
for tag, lines in dict_consolidated_scopes.items():
  dict_consolidated_scopes[tag] = os.linesep.join(lines)
@
```

Import the `os` module.

```python
<<imports>>+
import os
@
```

### Set up executable version.

Define the executable source.

```python
<<./litbop/litbop.py>>=
#!./<<virt_python>>

import sys
import liblitbop

if __name__ == "__main__":
  filename = sys.argv[1:][0]
  print(liblitbop.parse(open(filename, 'r').read()))
@
```

### Configure setup.py file.

```python
<<./litbop/setup.py>>=
import setuptools

setuptools.setup(
  name="litbop",
  version="<<version>>",
  author="Stefan Eng",
  author_email="eng_steff@hotmail.com",
  packages=setuptools.find_packages(),
  description="Self-hosted literate programming toolbox",
  classifers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    "Operating System :: Unix",
  ]
)
@
```

Copy `litbop.py` to `./bin/litbop2`

```shell
<<exec>>+
cp ./litbop/litbop.py ./bin/litbop2
@
```

Add executable permissions to the script.

```shell
<<exec>>+
chmod +x ./bin/litbop2
@
```

Create script that handles setup of virtual environment.

```python
<<./scripts/setup_virtualenv.py>>=
#!/usr/bin/env python3
import os
import venv
import subprocess
path_dir_virt = "<<dir_virtual_environment>>"
if not os.path.isdir(path_dir_virt):
  venv.create(path_dir_virt, with_pip=True)
  subprocess.call("<<virt_python>> -m pip install --upgrade pip".split())
  subprocess.call("<<virt_python>> -m pip install -e litbop".split())
@
```

Create virtual environment if there isn't one.

```shell
<<exec>>+
python scripts/setup_virtualenv.py
@
```

Define path to virtual python executable.
```shell
<<virt_python>>=
<<dir_virtual_environment>>/bin/python
@
```

Define the name of the directory containing the virtual environment.
```shell
<<dir_virtual_environment>>=
virt
@
```

Set the version.

```python
<<version>>=
0.0.1
@
```
