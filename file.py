import tempfile
import os
import uuid


class File:
    def __init__(self, path):
        self.path = path
        self.current_symbol = 0
        if not os.path.exists(path):
            with open(path, 'x'):
                pass

    def write(self, value):
        with open(self.path, 'w') as f:
            f.write(value)

    def read_all(self):
        with open(self.path, 'r') as f:
            return ''.join(f.readlines())

    def __add__(self, other):
        new_path = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()) + '.txt')
        with open(new_path, 'x') as f:
            f.write(self.read_all())
            f.write(other.read_all())

        return File(new_path)

    def __str__(self):
        return self.path

    def __iter__(self):
        return self

    def __next__(self):
        with open(self.path, 'r') as f:
            f.seek(self.current_symbol)
            row = f.readline().strip()
            if not row:
                raise StopIteration
            self.current_symbol += f.tell()
        return row


if __name__ == "__main__":
    file1 = File('file1.txt')
    file1.write("vvvvv\n")
    file1.write("nnnnnnn\n")

    file2 = File('file2.txt')
    file2.write("bbbbbbb\n")

    file3 = file1 + file2

    print(file3)

    for row in file3:
        print(row)
