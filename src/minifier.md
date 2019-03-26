# Python minifier literate source file.

Is it possible to read the generated bootstrapped code, minify it, and paste it
to the end of the `Readme.md` file?

Set up executable variant based on `libminify` library.

```python
<<./bin/minify>>=
#!/usr/bin/env python3
import sys

from parser.lib import libminify

if __name__ == "__main__":
  filename = sys.argv[1:][0]
  with open(filename, 'r') as fh:
    print(libminify.minify(fh.read()))
@
```

Make `./bin/minify` executable.

```shell
<<exec>>=
chmod +x ./bin/minify
@
```

Add `bin` directory to `.gitignore.`.

```shell
<<.gitignore, 'a'>>=
bin
@
```

Add the actual library file.

```python
<<./parser/lib/libminipy.py>>=
pass
@
```
