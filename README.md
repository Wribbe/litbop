'''
# Welcome.

This is the repository for **litbop** -- **lit**erate **bo**otstrapped **p**ython.

**litpop** is a:
* Self-hosting<sup>[wiki](https://en.wikipedia.org/wiki/Self-hosting)</sup>
* Language agnostic<sup>[stackExchange](https://softwareengineering.stackexchange.com/a/28498)</sup>
* Literate programming<sup>[wiki](https://en.wikipedia.org/wiki/Literate_programming)</sup> toolbox
* written in Python3.x<sup>[homepage](https://python.org)</sup>

(Quick summary of the terms [below](#what).)

## HowTo:

### Step-by-step quickstart:
  1. Make sure that `python` (>3.6) is available.
  2. Run `python3 README.md`
  3. Run `./litbop <literate-text-file(s)>`

### Write literate code:

See the [writing the parser](#writing-the-parser) section.

## What:

> **Self-hosting** is the use of a computer program as part of the toolchain or
> operating system that produces new versions of that same program—for example, a
> compiler that can compile its own source code.
-- [Wikipedia](https://en.wikipedia.org/wiki/Self-hosting)

> **Literate programming** is a programming paradigm introduced by Donald Knuth in
> which a program is given as an explanation of the program logic in a natural
> language, such as English, interspersed with snippets of macros and traditional
> source code, from which a compilable source code can be generated.
-- [Wikipedia](https://en.wikipedia.org/wiki/Literate_programming)

> **Language agnostic** refers to aspects of programming that are independent of any
> specific programming language. At least, that's how I've heard it used for the
> last thirty years.
-- [StackExchange](https://softwareengineering.stackexchange.com/a/28498)

## Why:

For me, the idea of literate programming is immensely intriguing ever since I
first heard of it. I can't remember where I first stumbled over it, but possible
contenders include:
> **Physically Based Rendering**, Third Edition describes both the mathematical
> theory behind a modern photorealistic rendering system as well as its
> practical implementation. A method known as “literate programming” combines
> human-readable documentation and source code into a single reference that is
> specifically designed to aid comprehension. Through the ideas and software in
> this book, you will learn to design and employ a full-featured rendering
> system for creating stunning imagery. Physically Based Rendering
-- [pbrt.org](https://www.pbrt.org)

> **Haskell and literate programming**
> Haskell is one of the few languages that provides native features to support
> literate programming. In haskell, a literate program is one with the suffix
> .lhs rather than .hs.
-- [haskell.org](https://wiki.haskell.org/Literate_programming)

> **noweb** is a literate programming tool, created in 1989–1999 by Norman Ramsey,
> and designed to be simple, easily extensible and language independent.
-- [Wikipedia](https://en.wikipedia.org/wiki/Noweb)

At least once a year I try to setup and use literate programming for a smaller
project, but it always peters out.

### Here we go again!

Then, last week I found the minimalistic github-repo for
[noweb.py](https://github.com/JonathanAquino/noweb.py)
which is hosting the code associated with this
[blogpost](http://jonaquino.blogspot.com/2010/04/nowebpy-or-worlds-first-executable-blog.html)
and thought the idea of a self-hosted literary program that assembles itself
was a superbly wonderful idea. The only thing that bothered me was that it could not
run itself straight of the bat, so I gave that a shot, and now we are here.

### Markdown as a ... code-medium?

While poking around with the code in a `.txt` format worked fine, it felt a bit
barren when uploaded to Github. I added a `README.md` and wrote some comments,
and thought; _couldn't the code be in here to??_, which I then tried, and it worked
better than expected. I'm using Markdown since it makes the source easy to convert
to other formats through [pandoc](https://pandoc.org) and renders nicely in the
repository on Github, but you can of course use any other python-readable text
format you want.

## Writing the parser:

### Output to files:

Lets begin with defining a `.gitignore` file for this repository.
```
<<.gitignore>>=
.gitignore
@
```
This will result in the text `.gitignore` being written to the file
`./.gitignore`, making the repository ignoring the file. This might seem a
bit redundant at the moment, but we'll get back to this later.

The main goal is to write a more readable version of the bootstrapping code
defined at the end of the document to the file `./bin/litbop_bootstrapped`,
using litbop and literal programming. First, lets define the file itself
together with its shebang, docstring and general structure.

```python
<<./bin/litbop_bootstrapped>>=
#!/usr/bin/env python3
""" Readable version of litbop bootstrapper code. """
<<import modules>>

def main(args):
  for filename in args:
    <<parse and resolve tags>>
    <<write source files to disk>>
  <<execute shell commands>>

if __name__ == "__main__":
  <<read arguments from commandline>>
  main(args)
@
```

Notice the `./bin/` part of the previously defined tag, litbop accepts any *nix
path on the format `<dir1>/.../<dirN>/<file>`, creating any missing
directories. If the file defined in the path already exists, litbop will
replace it without warning.

The parser will only try to create files out of tags that have a `.` in them,
which is usually automatically the case with source files like `.py` or `.c`.
However, if you want to write to a file to the project-root that does not have
a `.` in its name, i.e. a `Makefile`, you wold have to name it `./Makefile` to
sort it out.

### Defining tags:

Tags ending with `=` are definitions. The parser will take everything between
the `=` and `@` to mean the definition of the tagname,
`bin/litbop_bootstrapped` in this case. Tags without a trailing `=` or `+`
are substitution tags, and the parser will try to replace them with their
corresponding definition. If there is no definition for a tag, the unmodified
tag will be written to file without substitution.

### Appending to defined tags:

Since the code now creates the output directory `out` for us, lets add that to
the ignore file in order to avoid committing generated code to the repository.

```python
<<.gitignore>>+
litbop
@
```

The complete content of the `.gitignore` is now defined as:
```
.gitignore
litbop
```

Any tag with a trailing `+` will append to a previously defined tag with the same
name. Definitions and appends for the same tag-name do not need to be in
proximity of each other. When a tag is substituted, the definition, together
with any appends will be concatenated and replace the tag in question.

### Reading arguments from the command line:

The main idea is that the parser should parse and assemble source files based
on any file or files that are passed to it.

```python
<<read arguments from commandline>>=
args = sys.argv[1:]
@
```

Import the `sys` module.

```python
<<import modules>>=
import sys
@
```

### Non sequentiality, nested tags and indentation:

Lets jump to the part where the files are written in order to demonstrate the
capabilities of working with different parts of the code out of order. First
lets define up the `write source files to disk` tag into a for-loop and
sub-tags.

```python
<<write source files to disk>>=
for path_file, content_file in data_file_resolved.items():
  <<create dir structure if missing>>
  <<write content to filepath>>
@
```

Running `python README.md` right now, together with `cat
bin/litbop_bootstrapped` would produce the following output:

```python
#!/usr/bin/env python3
""" Readable version of litbop bootstrapper code. """
import sys

def main(args):
  for filename in args:
    <<parse and resolve tags>>
    for path_file, content_file in data_file_resolved.items():
      <<create dir structure if missing>>
      <<write content to filepath>>

if __name__ == "__main__":
  args = sys.argv[1:]
  main(args)
```

Since the tag `write source files to disk` is defined, it is replaced by the
definition at the indentation level that the tag had. Also notice that all the
definitions written this far have replaced their tags and undefined tags remain
unchanged. Lets leave it like that for now.

### Parsing and resolving tags:

In order to find the tag segments, this solution uses regular expressions,
available through the `re` module.

```python
<<import modules>>+
import re
@
```

The following defines regular expression matches for a regular tag, a
defining or appending tag, and a match for a tag-scope.

```python
<<defined regexes>>=
# Define regular expression matches for tags and scopes.
re_tag_match = "<<.*?>>"
re_tag_def_match = f"{re_tag_match}[+=]"
re_tag_scope = fr"^({re_tag_def_match})\s*(.*?)\s*^@"
@
```

After reading the data from the file, `re.findall()` can be used to find
all the scopes in the current data. The `re.DOTALL` is necessary in order to
make the `.*` match include newlines, which is needed to capture the whole
scope.

```python
<<parse and resolve tags>>=
<<defined regexes>>
data_file = open(filename).read()
data_tag_scopes = re.findall(re_tag_scope, data_file, re.DOTALL+re.MULTILINE)
@
```

Having a list of `(tag-name, scope-text)` tuples, all the appends need to be
consolidated with the corresponding define tag. Since they have the same name,
stripping the last character and concatenating their scopes into another
dictionary works fine.

First, create a dictionary keyed on the tag-names, with a value of the empty
list `[]`. Since the tags are on the form `<<tag-name>>c` where `c` is an
additional character stripping the first two characters and the last three
with: `tag[0:-1]` results in `<<tag-name>>` being returned.

```python
<<parse and resolve tags>>+
data_concatenated_tags = {k[0:-1]:[] for k,s in data_tag_scopes}
@
```

Iterate through the different tags and append them to the corresponding list.

```python
<<parse and resolve tags>>+
for tag, data in data_tag_scopes:
  tag_stripped = tag[0:-1]
  data_concatenated_tags[tag_stripped].append(data)
@
```

Create strings of all the lists by `join`ing with `os.linesep`.

```python
<<parse and resolve tags>>+
for tag, lines in data_concatenated_tags.items():
  data_concatenated_tags[tag] = os.linesep.join(lines)
@
```

### Resolving nested tags.

Since there is no limit on the number of number of possible nested tags, the
substitution process needs to keep going until there are no new changes.

```python
<<parse and resolve tags>>+
# Re-use the data_concatenated_tags dictionary.
data_file_resolved = data_concatenated_tags
while True:
  <<hash the current dictionary>>
  <<substitute the current visible tags>>
  <<re-hash and break if nothing changed>>
<<strip tags in resolved dict>>
@
```

For this purpose, hashing naively, using the built-in `hash()` and `str()`
methods works fine.

```python
<<hash the current dictionary>>=
hash_before = hash(str(data_file_resolved))
@
```

Iterate over all the current tags and do the following.

```python
<<substitute the current visible tags>>=
for tag, data in data_file_resolved.items():
  <<extract indentation and nested tags>>
  <<iterate over and substitute found tags>>
  <<write data back to dictionary>>
@
```

Match and capture any leading whitespace, then match and capture the tag. If
there are any trailing whitespace, match them but discard it.

```python
<<extract indentation and nested tags>>=
indent_and_tags = re.findall(
  f"({re_whitespace}*)({re_tag_match}){re_whitespace}*", data
)
@
```

Check if there is data that should replace the tag. If the data exists,
add the indentation for the tag to each line of the new data. Update the `data`
variable with the substituted data.

```python
<<iterate over and substitute found tags>>=
for indent, tag_to_replace in indent_and_tags:
  data_replace = data_file_resolved.get(tag_to_replace)
  if not data_replace:
    continue
  data_replace = os.linesep.join(
    [indent+line for line in data_replace.strip().splitlines()]
  )
  # Re-add escaped backslashes.
  data_replace = data_replace.replace("\\", "\\\\")
  data = re.sub(f"({re_whitespace}*){tag_to_replace}", data_replace, data)
@
```

Write the updated data back to the `data_file_resolved` dictionary.

```python
<<write data back to dictionary>>=
data_file_resolved[tag] = data
@
```

Don't forget to define `re_whitespace` since it is used above.

```python
<<defined regexes>>+
re_whitespace = r"[ \\t]"
@
```

Re-hash the updated dictionary and break if nothing has changed.

```python
<<re-hash and break if nothing changed>>=
hash_after = hash(str(data_file_resolved))
if hash_after == hash_before:
  break
@
```

Strip the tags and avoid including any regular expression read from non-source
or bootstrapping code.

```python
<<strip tags in resolved dict>>=
dict_new = {}
for tag, data in data_file_resolved.items():
  if '*' in tag:
    continue
  tag_stripped = tag[2:-2]
  dict_new[tag_stripped] = data
data_file_resolved = dict_new
@
```

### Writing to disk.

Anything that has a `.` is deemed to be a file, otherwise continue.

```python
<<create dir structure if missing>>=
if not '.' in path_file:
  continue
@
```

Iterating over the dictionary, check that the directories in the file path (if
there are any) exists, otherwise create them.

```python
<<create dir structure if missing>>=
path_dir = os.path.dirname(path_file)
if path_dir and not os.path.isdir(path_dir):
  os.makedirs(path_dir)
@
```

In order to make this work, import the `os` module.

```python
<<import modules>>+
import os
@
```

Finally, write the data to disk.

```python
<<write content to filepath>>=
with open(path_file, 'w') as fh:
  fh.write(content_file.strip()+os.linesep)
@
```

### Ability to run shell-functions from snippet.

Define an `exec` tag, this will be executed by the parser.

```shell
<<exec>>=
chmod +x ./bin/litbop_bootstrapped
ln -rsf ./bin/litbop_bootstrapped ./bin/litbop
@
```

If there are any commands defined in the `exec` tag, execute them. The
assumption is that there is one command per line in the supplied data.

```python
<<execute shell commands>>=
commands = data_file_resolved.get('exec')
if not commands:
  return
for command in commands.splitlines():
  subprocess.run(command.split())
@
```

Import the subprocess module.

```python
<<import modules>>+
import subprocess
@
```


# The bootstrapping code.

This is the end of the document, and the **very** unreadable code below,
together with the absolutely last line, is what makes this little project tick.
Might have gotten a bit carried away when trying to minimize it, one should
probably not do __*ANYTHING*__ of what is done below, don't use as reference!

```python
import re, os; from re import S,M; from os.path import dirname as opd!rs,rt,nj
,d,rf=[r"[ \t]","<<.*?>>",'\n'.join,open(__file__).read(),re.findall]!dt={t:''
.join(rf(f"{t}[+=]\s?(.*?)^@",d,S+M)) for t in rf(f"({rt}).*?^@",d,S+M)}!while
 True:!qdh = hash(str(dt))!qfor k,v in dt.items():!qqfor i,t in [t for t in rf
(f"({rs}*)({rt}){rs}?",v,S) if t[1] in dt]:!qqqdt[k] = re.sub(f"{rs}*"+t,nj([i
+l for l in dt[t].replace('\\', '\\\\').splitlines()]),dt[k])!qif dh == hash(s
tr(dt)):!qqdt = {k[2:-2]:v for k,v in dt.items() if '*' not in k}; break!for d
n,k,v in [(opd(k),k,v) for k,v in dt.items() if '.' in k]:!qif dn and not os.p
ath.isdir(dn):!qqos.makedirs(dn)!qopen(k,'w').write(v)!import subprocess as sp
; [sp.run(c.split()) for c in dt['exec'].splitlines()]!```'''
d=open(__file__).read()[-876:-110];d=d.replace('q','  ').replace('\n','')\
.replace('!','\n');exec(d)
