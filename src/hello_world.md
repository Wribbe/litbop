# This is a small test file.

Define main method.

```python
<<out/hello_world.py>>=
def main():
  <<print hello world>>
<<setup main runtime>>
@
```

Set up main runtime.

```python
<<setup main runtime>>=
if __name__ == "__main__":
  main()
@
```

Print hello world.

```python
<<print hello world>>=
print("HELLO WORLD!")
@
```
