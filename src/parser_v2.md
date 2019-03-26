# Literate source for extended bootstrapped parser.

### Additions - Todo:
* [ ] - Support `<<path_file, 'a'>>` syntax for appending to existing files.
* [ ] - Support dynamic variables with `<<{{ignore_file}}, 'w'>>` syntax.

### Defining the main structure of the lib.

```python
<<./parser/lib/liblitbop2.py>>=
<<imports>>
<<global definitions>>
<<helper methods>>
def parse(data):
  <<regexes>>
  <<find tags and scopes>>
  <<consolidate tags>>
  <<parse and process tags>>
  <<write data to disk>>
@
```

Make sure there is a `__init__.py` file in the `lib` and `parser` directories.

```python
<<./parser/lib/__init__.py>>=
# File needed to make lib a module.
@
```

```python
<<./parser/__init__.py>>=
# File needed to make parser a module.
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

Defining the stub for the first helper method, to be resolved later:

```python
<<helper_process_tag>>=
def process_tag(tag):
  <<identify tag type>>
  <<proceed with doing the correct thing>>
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

### Set up executable version.

Define the executable source.

```python
<<./bin/litbop2>>=
#!/usr/bin/env python3

import sys

from parser.lib import liblitbop2

if __name__ == "__main__":
  filename = sys.argv[1:][0]
  print(liblitbop2.parse(open(filename, 'r').read()))
@
```

Add executable permissions to the script.

```shell
<<exec>>=
chmod +x ./bin/litbop2
@
```
