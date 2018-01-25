class Value:
    def __init__(self, amount = None):
        self.amount = amount or 0
    
    def __get__(self, obj, obj_type):
        return self.amount
    
    def __set__(self, obj, value):
        if hasattr(obj, 'commission'):
            self.amount = value - value * obj.commission
        else:
            self.amount = value