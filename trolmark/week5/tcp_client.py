import asyncio

from utilities import Response_Parser, ResponseFormatter,Put_Request,Get_Request

class ClientError(Exception):
    pass

class Client():
    def __init__(self, host, port, timeout = None):
        self.host = host
        self.port = port
        self.timeout = timeout or 15
        
        self.loop = asyncio.get_event_loop()
        self.parser = Response_Parser()
        self.formatter = ResponseFormatter()
        
    def put(self, metrics_name, metrics_value, timestamp = None):
        request = Put_Request(metrics_name, metrics_value, timestamp)
        self.push_request(request)
        
    def get(self, metrics_name):
        request = Get_Request(metrics_name)
        response_data = self.push_request(request)
        return self.formatter.format_get_response(response_data)

    
    def push_request(self, request):
        response = self.send(request.encode())
        response_data = self.parser.parse_response(response)
        if response_data is None or response_data.is_error:
            raise ClientError()
        return response_data.result
        
    def send(self, message):
        future = asyncio.Future()
        coro = self.loop.create_connection(
            lambda: ClientProtocol(message, self.loop, future), self.host, self.port
        )

        asyncio.ensure_future(coro)
        self.loop.run_until_complete(asyncio.wait_for(future, self.timeout))
        return future.result()
        

class ClientProtocol(asyncio.Protocol):
    def __init__(self, message, loop, future):
        self.message = message
        self.loop = loop
        self.future = future

    def connection_made(self, transport):
        transport.write(self.message.encode())

    def data_received(self, data):
        self.future.set_result(data.decode())

    def connection_lost(self, exc):
        print('The server closed the connection')
        self.loop.stop()
        
        
def run_client(host, port, timeout):
    client = Client(host, port, timeout)
    client.put("test", 0.5, 1)
    client.put("test", 0.2, 2)
    client.put("load", 301, 3)
    client.get("not_exist")
    print(client.get("test"))
    print(client.get("*"))
    
if __name__ == '__main__':
    run_client("127.0.0.1",1818, 2)