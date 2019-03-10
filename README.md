"""
# Literal python.

This is an attempt to write a more verbose version of the "self-hosted" literal
programming code that is at the bottom of this file. In other words, when
running this file with `python README.md` it should produce a python program
that is a more well-structured version of the code defined at the end of this
file.

```python
<<out/hello_world.py>>=
<<say hello world>>
@
```

```python
<<say hello world>>=
print("HELLO1")
@
```

```python
<<say hello world>>+
print("HELLO2")
@
```

```python
<<say hello world>>+
print("HELLO3")
@
```

Defining the structure of the final output file.

```python
<<out/literal_python.py>>=

<<import modules>>

def main(args):
  <<setup dictionary of tags>>
  <<do a recursive replace of all the tags>>
  <<write all defined files to disk>>

if __name__ == "__main__":
  <<read command line arguments>>
  main(args)
@
```

Let's begin with defining what is read from the command line.
First we need to import the sys module in order to read the command line
arguments.

```python
<<import modules>>=
import sys
@
```

Assuming the arguments consists of a list of files that should be parsed, we
pass them along, removing the name of the currently running file at index 0.

```python
<<read command line arguments>>=
args = sys.argv[1:]
@
```

We probably want to keep each files namespace isolated, which means a
dictionary per filename in the passed along list of files.

```python
<<setup dictionary of tags>>=
dictionaries = []
for filename in args:
  with open(filename, 'r') as fh:
    data_file = fh.read()
    <<construct list of tags>>
    <<add to dictionaries list>>
@
```

In order to support both the define `>>=` and append `>>+` syntax, all the
defines and appends tags need to be merged together.

```python
<<construct list of tags>>=
<<find all scopes and tags>>
<<merge all tags>>
@
```

## Housekeeping.

I want a `.gitignore` file.

```
<<.gitignore>>=
Makefile
out
*.pdf
*.html
*.tex
.gitignore
@
```

I want a `Makefile`.

```make
<<./Makefile>>=
@
```

# The bootstrapping part.

This is the end of the document, and the **very** unreadable code beneath,
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
"""
exec(''.join(open(__file__).readlines()[-18:-3]))
