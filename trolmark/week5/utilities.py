import asyncio
import time
import operator


class Storage():
    def __init__(self):
         self.storage = {}
         
    def save_request(self, request):
        value = (request.metrics_value, request.timestamp)
        self.storage = self.save_to_storage(request.metrics_name, value, self.storage) 
    
    def load_value_by_request(self, request):
        if request.request_all:
            return self.storage
        if request.metrics_name not in self.storage:
            return None
        return {request.metrics_name : self.storage[request.metrics_name] }
    
    
    def save_to_storage(self, metrics_name, value, storage):
        if metrics_name not in storage:
            storage[metrics_name] = [value]
            return storage
  
        existed_metrics = storage[metrics_name]     
        storage[metrics_name] = self.pre_process_value(value, existed_metrics)
        return storage
    
    def pre_process_value(self, value, metrics):
        # remove duplicates with same timestamp
        converted_values = list(filter(lambda tup: tup[1] != value[1], metrics))
        # sort by value
        sorted_values = sorted(converted_values + [value], key=lambda tup: tup[1])
        return sorted_values

class ResponseFormatter():

    def format_get_response(self, response):
        if not response:
            return {}
        return self.format_response(response)
      
    def format_response(self, response):
        result = {}
        for item in response:
            key = item[0]
            metrics = [(int(item[2]), float(item[1]))]           
            if key not in result:
                result[key] = metrics
            else:
                result[key] += metrics
        return dict(sorted(result.items(), key=operator.itemgetter(1)))
    
class Get_Request():
    def __init__(self, metrics_name):
        self.metrics_name = metrics_name
        if metrics_name == "*":
            self.request_all = True
        else:
            self.request_all = False
    
    def encode(self):
        return "get {key}\n".format(
            key = self.metrics_name
        )
    
    @staticmethod
    def decode_all_request():
        return Get_Request("*")
    
    @staticmethod
    def decode_request(request):
        key = request.split(" ")[1]
        return Get_Request(metrics_name = key)
    
class Put_Request():
    def __init__(self, metrics_name, metrics_value, timestamp = None):
        self.timestamp = timestamp or str(int(time.time()))
        self.metrics_name = metrics_name
        self.metrics_value = metrics_value
    
    def encode(self):
        return "put {key} {value} {timestamp}\n".format(
            key = self.metrics_name,
            value = self.metrics_value,
            timestamp = self.timestamp
        )
    
    @staticmethod
    def decode_request(request):
        components = request.split(" ")
        if len(components) > 3 : 
            return Put_Request(components[1], components[2], components[3])
        return None

    
class Request_Parser():
   
    def parse_request(self, request):
        request = self.clean_request(request)
        if self.is_get_all_request(request):
            return Get_Request.decode_all_request()
        elif self.is_get_request(request):
            return Get_Request.decode_request(request)
        elif self.is_put_request(request):
            return Put_Request.decode_request(request)
    
    def is_get_request(self, request):
        return request.startswith("get")    
    
    def is_get_all_request(self, request):
        return self.is_get_request(request) and request.endswith("*")
    
    def is_put_request(self, request):
        return request.startswith("put")
    
    def clean_request(self, request):
        return request.replace('\r', '').replace('\n', '')
    
    
class Response_Result():
    def __init__(self, is_error, result = None):
        self.is_error = is_error
        self.result = result
    
class Response_Parser():

    def parse_response(self, raw_response):
        if self.is_error_response(raw_response):
            return Response_Result(is_error = True)
        elif self.is_success_response(raw_response):
            response_data = self.clean_response(raw_response)
            if not response_data:
                return Response_Result(is_error = False, result = {})
            # Parse data into tuples
            response = [tuple(x.split(' ')) for x in response_data.split('\n')]
            return Response_Result(is_error = False, result = response)
        else:
            return None
            
    def clean_response(self, request):
        return request\
            .replace('\r', '')\
            .replace('ok\n\n','')\
            .replace('ok\n', '')\
            .replace('\n\n', '')
        
    def is_success_response(self, request):
        return request.startswith("ok\n")
        
    def is_error_response(self, request):
        return request.startswith("error") 
    
    
class Response():
    def __init__(self, response_text, result = None):
        self.response_text = response_text
        self.result = result
        
    def stringify_result(self, result):
        client_compatible_result = ""
        for key,value in result.items():
            for item in value:
                client_compatible_result += str(key) + " " + " ".join(item) + "\n"
        return client_compatible_result
        
    def encode(self):
        if self.result:
            str_result = self.stringify_result(self.result)
            return self.response_text.encode() + str_result.encode() + "\n".encode()
        else:
            return self.response_text.encode()
    
    @staticmethod
    def failure():
        return Response("error\nwrong command\n\n")
    
    @staticmethod
    def success(result = None):
        if result:
            return Response("ok\n", result)
        else:
            return Response("ok\n\n")