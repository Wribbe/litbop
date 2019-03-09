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
ls = zip(*[' '*i+open(__file__).read()+' '*(2-i) for i in range(3)])
d = [i for i,(c1,c2,c3) in enumerate(ls) if c1+c2=="<<" or c2+c3==">>"]
print(d)
#print([(c1,c2,c3) for zip(

#print([i if c == "=" else 0 for i,c in enumerate(open(__file__).read())])
