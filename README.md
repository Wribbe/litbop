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
  3. Run `python3 out/litbop_bootsrapped.py <literate-text-file(s)>`

### Write literate code:

See the [syntax](#syntax) section.

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
first heard of it. Can't remember where I stumbled over it first, but possible
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

I feel there is this constant pull towards literate programming. At least once a year
I try to setup and use literate programming for a smaller project, but it
always peters out.

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

## Syntax:

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
defined at the end of the document to the file `./out/litbop_bootstrapped.py`,
using litbop and literal programming. First, lets define the file itself
together with its shebang, docstring and general structure.

```python
<<out/litbop_bootstrapped.py>>=
#!/usr/bin/env python3
""" Readable version of litbop bootstrapper code. """
<<import modules>>

def main(args):
  <<read files from args>>
  <<find and resolve tags>>
  <<write files to disk>>

if __name__ == "__main__":
  <<read arguments from commandline>>
  <<call main method>>
@
```

Tags ending with `=` are definitions. The parser will take everything between
the `=` and `@` to mean the definition of the tagname,
`out/litbop_bootstrapped.py` in this case. The tags above without a trailing
`=` are substitution tags which means, if they are defined somewhere in the
file, the tag will be replaced with its corresponding definition. In the case of
using a tag that is not yet defined, the unmodified tag will be written to the
file in question.

Notice the `out/` part of the previously defined tag. Litbop will accept any
*nix path on the format `<dir1>/.../<dirN>/<file>` and create the
nested directory-structure if it does not already exist, and write to the
given `<file>`, replacing anything that already exists. The parser will only
try to create files out of tags that have a `.` in them, which is usually
automatically the case with source files like `.py` or `.c`. However, if you
want to write to a file to the project-root that does not have a `.` in its
name, i.e. a `Makefile`, you wold have to name it `./Makefile` to sort it out.

Since the code now creates the output directory `out` for us, lets add that to
the ignore file in order to avoid committing generated code to the repository.

```python
<<.gitignore>>+
out/
@
```

The complete content of the `.gitignore` is no defined as:
```
.gitignore
out/
```

# The bootstrapping code.

This is the end of the document, and the **very** unreadable code below,
together with the absolutely last line, is what makes this little project tick.
Might have gotten a bit carried away when trying to minimize it, one should
probably not do __*ANYTHING*__ of what is done below, don't use as reference!

```python
import re, os; from re import S as rS; from os.path import dirname as opd
rs,rt,nj,dd,rf=[r"[ \t]","<<.*?>>",'\n'.join,open(__file__).read(),re.findall]
dt={t:''.join(rf(f"{t}[+=]\s?(.*?)@",dd,rS)) for t in rf(f"({rt}).*?@",dd,rS)}

while True:
  dh = hash(str(dt))
  for k,v in dt.items():
    for i,t in [t for t in rf(f"({rs}*)({rt}){rs}?",v,rS) if t[1] in dt]:
      dt[k] = re.sub(f"{rs}*"+t,nj([i+l for l in dt[t].splitlines()]),dt[k])
  if dh == hash(str(dt)):
    dt = {k[2:-2]:v for k,v in dt.items() if '*' not in k}; break
for dn,k,v in [(opd(k),k,v) for k,v in dt.items() if '.' in k]:
  if dn and not os.path.isdir(dn):
    os.makedirs(dn)
  open(k,'w').write(v)
```
'''
exec(''.join(open(__file__).readlines()[-18:-3]))
