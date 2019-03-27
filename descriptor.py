class Value:

    def __init__(self):
        self.value = 0

    def __get__(self, instance, owner):
        return int(self.value)

    def __set__(self, instance, value):
        commission = value * instance.commission
        self.value = value - commission


class Account:
    amount = Value()

    def __init__(self, commission):
        self.commission = commission


if __name__ == "__main__":
    new_account = Account(0.2)
    new_account.amount = 100

    print(new_account.amount)
