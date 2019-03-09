fr"""

This is an attempt to write a more verbose version of the "self-hosted" literal
programming code that is at the bottom of this file. In other words, when
running this file with `python {__file__}` it should produce a python program
that is a more well-structured version of the code defined at the end of this
file.

Defining the structure of the final output file.

<<literal_python.py>>=

<<import modules>>

def main(args):
  <<setup dictionary of tags>>
  <<do a recursive replace of all the tags>>
  <<write all defined files to disk>>

if __name__ == "__main__":
  <<read command line arguments>>
  main(args)
@

Let's begin with defining what is read from the command line.
First we need to import the sys module in order to read the command line
arguments.

<<import modules>>=
import sys
@

Assuming the arguments consists of a list of files that should be parsed, we
pass them along, removing the name of the currently running file at index 0.

<<read command line arguments>>=
args = sys.argv[1:]
@

We probably want to keep each files namespace isolated, which means a
dictionary per filename in the passed along list of files.

<<setup dictionary of tags>>=
dictionaries = []
for filename in args:
  with open(filename, 'r') as fh:
    data_file = fh.read()
    <<construct list of tags>>
    <<add to dictionaries list>>
@

In order to support both the define `>>=` and append `>>+` syntax, all the
defines and appends tags need to be merged together.

<<construct list of tags>>=
<<find all scopes and tags>>
<<merge all tags>>
@
"""
import re, os
ms=[m.split('\n',1) for m in re.findall(r"<<.*?@",open(__file__).read(),re.S)[:-1]]
md={k[:-1]:'' for k,v in ms}
for k,v in ms:
  md[k[:-1]] += v[:-1]
h_prev=None
while True:
  h_prev=hash(str(md))
  for k,v in md.items():
    for pat,sub in md.items():
      ind = [m.strip('\n') for m in re.findall(rf"\s+{pat}",v)]
      if ind:
        ind = len(ind[0]) - len(ind[0].lstrip())
        ls = sub.splitlines()
        sub = os.linesep.join(ls[:1] + [' '*ind+l.strip() for l in ls[1:]])
      md[k] = re.sub(pat,sub,md[k])
  if h_prev == hash(str(md)):
    break
if not os.path.isdir("out"):
  os.makedirs("out")
for k,v in md.items():
  if '.' in k:
    open(os.path.join("out", k[2:-2]), 'w').write(v)
