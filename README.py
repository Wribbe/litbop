"""
This is some text that should not be parsed as code.

<<say hello world>>=
print("Hello World")
@

Try to add to the hello world section by using the `>>+` syntax.

<<say hello world>>+
print("Addition to hello world.")
@

These should all add up in the end, ensure they do.

<<say hello world>>+
print("Second addition to hello world.")
@

Define the file that uses the say hello world segment.

<<hello_world.py>>=
def main():
  # Comment that should stay in palace.
  <<say hello world>>
if __name__ == "__main__":
  main()
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
