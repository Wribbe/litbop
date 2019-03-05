"""
This is some text that should not be parsed as code.

<<hello world.py>>=
def main():
  <<say hello world>>
if __name__ == "__main__":
  main()
@

<<say hello world>>=
print("Hello World")
@
"""

import os

tags = {}
lines = [line.rstrip() for line in open(__file__).readlines()]

DIR_OUT = "out"

def_tag = None
for line in lines:
  line_stripped = line.strip()
  if line_stripped.startswith("<<"):
    if line_stripped.endswith("="):
      def_tag = line_stripped
  if def_tag:
    lines_in_def = tags.get(def_tag)
    if not lines_in_def:
      lines_in_def = tags[def_tag] = []
    lines_in_def.append(line)
  if line_stripped == "@":
    def_tag = None

while True:
  hash_tags_prev = hash(str(tags))
  for tag, lines in tags.items():
    new_lines = []
    for line in lines:
      line_stripped = line.strip()
      if line_stripped.startswith("<<") and line_stripped.endswith(">>"):
        ind = ' '*(len(line) - len(line.lstrip()))
        lines_in_tag = [f"{ind}{l}" for l in tags[f"{line_stripped}="][1:-1]]
        new_lines += lines_in_tag
      else:
        new_lines.append(line)
    tags[tag] = new_lines
  hash_tags_current = hash(str(tags))

  if hash_tags_current == hash_tags_prev:
    break

if not os.path.isdir(DIR_OUT):
  os.makedirs(DIR_OUT)
for key, lines in tags.items():
  if '.' in key and '=' in key:
    filename = key[2:-3]
    with open(os.path.join(DIR_OUT, filename), 'w') as fh:
      fh.write(os.linesep.join(lines[1:-1]))
