class FileReader:
    def __init__(self, path=None):
        self.path = path

    def read(self):
        try:
            with open(self.path) as f:
                result = "".join(f.readlines())
        except IOError:
            result = ""
        return result


if __name__ == "__main__":
    reader = FileReader("example.txt")
    print(reader.read())

