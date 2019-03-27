import csv
import os

class CarBase:
    car_type = None

    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying) if is_float(carrying) else 0.0

    def get_car_type(self):
        return self.car_type

    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)[1]

    def __str__(self):
        return "Class {0}: car_type = {1}, brand = {2}, photo_file_name = {3}, carrying = {4} "\
            .format(self.__class__, self.car_type, self.brand, self.photo_file_name, self.carrying)


class Car(CarBase):
    car_type = "car"

    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count) if passenger_seats_count.isdigit() else 0

    def __str__(self):
        return super().__str__() + "passenger_seats_count = {0}".format(self.passenger_seats_count)


class Truck(CarBase):
    car_type = "truck"

    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        self.body_width, self.body_height, self.body_length = self.split_body_whl(body_whl, 3, 'x')

    def get_body_volume(self):
        return self.body_height * self.body_length * self.body_width

    @staticmethod
    def split_body_whl(body_whl, count, split):
        whl = []
        for s in body_whl.split(split):
            if s and is_float(s):
                whl.append(float(s))
            else:
                whl.append(0.0)

        while len(whl) < count:
            whl.append(0.0)

        return whl

    def __str__(self):
        return super().__str__() + "body_height = {0}, body_length = {1}, body_width = {2}"\
            .format(self.body_height, self.body_length, self.body_width)


class SpecMachine(CarBase):
    car_type = "spec_machine"

    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra

    def __str__(self):
        return super().__str__() + "extra = {0}".format(self.extra)


def get_car_list(csv_filename):
    car_list = []
    reader = read_line_csv(csv_filename)

    row = next(reader)
    while row:
        try:
            car_type = row[0]
            print("car_type = {0}, other = {1}".format(car_type, row[1:]))
            obj = None
            if car_type == Car.car_type:
                obj = Car(row[1], row[3], row[5], row[2])
            if car_type == Truck.car_type:
                obj = Truck(row[1], row[3], row[5], row[4])
            if car_type == SpecMachine.car_type:
                obj = SpecMachine(row[1], row[3], row[5], row[6])
        except Exception as e:
            print(e)

        if obj:
            car_list.append(obj)
        row = next(reader, None)
    return car_list


def read_line_csv(csv_filename):
    if not os.path.exists(csv_filename):
        raise FileNotFoundError("File {0} is not found".format(csv_filename))

    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)  # пропускаем заголовок
        for row in reader:
            yield row


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    car_list = get_car_list("cars.csv")
    print("Size = {0}".format(len(car_list)))
    for car in car_list:
        print(car)

    print(car_list[0].get_photo_file_ext())
    print(car_list[1].get_body_volume())



