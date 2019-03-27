import os

if os.fork() == 0:
    print(os.fork())
else:
    print(os.fork())