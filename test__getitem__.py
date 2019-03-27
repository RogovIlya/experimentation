class Item:

    def __init__(self, name, age):
        self.name = name
        self. age = age


    def __getitem__(self, item):
        print(item)
        return self.name


if __name__ == "__main__":
    item = Item("fff", 5)
    print(item[0])