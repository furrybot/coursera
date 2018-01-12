import json
from functools import wraps

def to_json(wrapped):
    @wraps(wrapped)
    def inner(*args, **kwargs):
        json_convertable_types = (list, dict, str, int, float, bool, type(None))
        result = wrapped(*args, **kwargs)
        if isinstance(result, json_convertable_types):
            json_result = json.dumps(result)
            return json_result
        return result
    return inner