# file one.py
def func():
    print("func() in one.py")

test = [5,4,3,2,1];

print("top-level in one.py")

if __name__ == "__main__":
    print("one.py is being run directly")
else:
    print("one.py is being imported into another module")