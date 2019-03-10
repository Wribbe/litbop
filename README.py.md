"""
This is some text that should not be parsed as a code

<<test.py>>=
```python
def main():
  ```print hello world```
```

wat?
<<print hello world>>=
```python
  print("HELLO WORLD")
```
"""
print(open(__file__).read())
