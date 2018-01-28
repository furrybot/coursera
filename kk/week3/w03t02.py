import csv
import io
import sys
import os


class CarType:
    car = 'car'
    truck = 'truck'
    spec_machine = 'spec_machine'


class CarBase:
    def __repr__(self):
        return '\n' + ', '.join(f"{key}: {value}" for key, value in vars(self).items()) + '\n'

    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = carrying

    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)[1]


class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = CarType.car
        self.passenger_seats_count = passenger_seats_count


class Truck(CarBase):
    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = CarType.truck
        self._parse_whl(body_whl)

    def _parse_whl(self, whl):
        default_whl = 0.0
        whl_parts = whl.split('x')
        if len(whl_parts) == 3:
            self.body_width = float(whl_parts[0])
            self.body_height = float(whl_parts[1])
            self.body_length = float(whl_parts[2])
        else:
            self.body_width = default_whl
            self.body_height = default_whl
            self.body_length = default_whl

    def get_body_volume(self):
        return self.body_width * self.body_height * self.body_length


class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = CarType.spec_machine
        self.extra = extra


class CarRowInfo:
    def __init__(self, row):
        self.row = row

    def is_correct(self): return len(self.row) >= 7

    def get_type(self): return self.row[0]

    def get_brand(self): return self.row[1]

    def get_photo_file_name(self): return self.row[3]

    def get_carrying(self): return float(self.row[5])

    def get_passenger_seats_count(self): return int(self.row[2])

    def get_body_whl(self): return self.row[4]

    def get_extra(self): return self.row[6]


class CarRowParser:
    make_me_a_car = {
        CarType.car: lambda row_info: Car(row_info.get_brand(), row_info.get_photo_file_name(), row_info.get_carrying(),
                                          row_info.get_passenger_seats_count()),
        CarType.truck: lambda row_info: Truck(row_info.get_brand(), row_info.get_photo_file_name(),
                                              row_info.get_carrying(), row_info.get_body_whl()),
        CarType.spec_machine: lambda row_info: SpecMachine(row_info.get_brand(), row_info.get_photo_file_name(),
                                                           row_info.get_carrying(), row_info.get_extra())
    }

    @classmethod
    def parse(cls, row_info: CarRowInfo):
        if not row_info.is_correct():
            return None
        car_type = row_info.get_type()
        if car_type in cls.make_me_a_car:
            try:
                return cls.make_me_a_car[car_type](row_info)
            except ValueError:
                return None
        else:
            return None


def get_car_list(csv_filename, encoding='utf-8'):
    car_list = []
    try:
        csv_fd = io.open(csv_filename, encoding=encoding)
    except IOError:
        print(f"Unable to open {csv_filename}")
        sys.exit(-1)

    reader = csv.reader(csv_fd, delimiter=';')
    next(reader)  # пропускаем заголовок
    for row in reader:
        vehicle = CarRowParser.parse(CarRowInfo(row))
        if vehicle is not None:
            car_list.append(vehicle)

    csv_fd.close()
    return car_list

