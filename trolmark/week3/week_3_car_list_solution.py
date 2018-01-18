from enum import Enum
import csv 
import os
import sys

class CarType(Enum):
    CAR = "car"
    TRUCK = "truck"
    SPEC_MACHINE = "spec_machine"
    NONE = "none"
        
    
class Photo:
    def __init__(self, name):
        self.value = name
        
    def extension(self):
        return os.path.splitext(self.value)[1]
    
    
class Identity:
    def __init__(self,v):
        self.value = v
    
    def bind(self, func):
        self.value = func(self.value)
        return self
    

# Utils functions
def load_raw_data(filename:None) -> list:
    if not os.path.isfile(filename) or filename is None:
        return []

    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        return [row for row in reader]
    
def parse_to_dict(data_list) -> list:
    if len(data_list) == 0 : return []
    
    titles = data_list.pop(0)
    return [dict(zip(titles, values)) for values in data_list
            if len(titles) == len(values)]

def map_to_car_model(model) -> dict:
    
    model_initializer_map = {
        CarType.CAR.value : Car.construct_from_dict,
        CarType.TRUCK.value : Truck.construct_from_dict,
        CarType.SPEC_MACHINE.value : SpecMachine.construct_from_dict
    }
    
    car_type = model["car_type"]
    if car_type not in model_initializer_map:
        return None

    return model_initializer_map[car_type](model)
    
def parse_to_models(raw_list) -> list:
    if len(raw_list) == 0 : return [] 
    
    models = map(map_to_car_model, raw_list)
    valid_models = filter(lambda x: x, list(models))
    return list(valid_models)
      
    

# Hierarchy of classes        
class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self._photo = Photo(photo_file_name)
        self.carrying = float(carrying)
        self._car_type = CarType.NONE
        
    def get_photo_file_ext(self) -> str:
        return self._photo.extension()

    @property
    def photo_file_name(self) -> str:
        return self._photo.value
    
    @property
    def car_type(self) -> str:
        return self._car_type.value
    

    
class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        
        self._car_type = CarType.CAR
        self.passenger_seats_count = passenger_seats_count
    
    @staticmethod
    def construct_from_dict(raw_model):
        passenger_seats_count = int(raw_model["passenger_seats_count"]) or 0
        return Car(raw_model["brand"], 
                   raw_model["photo_file_name"], 
                   raw_model["carrying"], 
                   passenger_seats_count)
        
        
class Truck(CarBase):
    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        
        self._car_type = CarType.TRUCK
        (self.body_width, self.body_height, self.body_length) = self.parse_body_params(body_whl,"x")
     
    def parse_body_params(self, body_whl = None, delimeter = None) -> (float, float, float):
        if not body_whl or delimeter is None:
            return (0, 0, 0)
        
        params = body_whl.split(delimeter)
        return (float(params[0]), float(params[1]), float(params[2]))
        
    @staticmethod
    def construct_from_dict(raw_model):
        return Truck(raw_model["brand"], 
                     raw_model["photo_file_name"], 
                     raw_model["carrying"], 
                     raw_model["body_whl"])
    
    def get_body_volume(self) -> float:
        return self.body_width * self.body_height * self.body_length


class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        
        self.extra = extra
        self._car_type = CarType.SPEC_MACHINE
        
    @staticmethod
    def construct_from_dict(raw_model):
        return SpecMachine(raw_model["brand"], 
                       raw_model["photo_file_name"], 
                       raw_model["carrying"], 
                       raw_model["extra"])


def get_car_list(csv_filename) -> list:
    return Identity(csv_filename)\
    .bind(load_raw_data)\
    .bind(parse_to_dict)\
    .bind(parse_to_models)\
    .value    
    
if __name__ == "__main__":
    get_car_list(sys.argv[1])
    