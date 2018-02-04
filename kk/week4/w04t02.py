class Value:
    def __set__(self, obj, val):
        self.val = val

    def __get__(self, obj, obj_type):
        return int(self.val - obj.commission * self.val) if hasattr(obj, 'commission') else self.val


class Account:
    amount = Value()

    def __init__(self, commission):
        self.commission = commission
