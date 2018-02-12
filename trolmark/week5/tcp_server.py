import asyncio
from utilities import Request_Parser,Put_Request,Get_Request, Response, Storage

class Server():
    def __init__(self, host, port):
        self.loop = asyncio.get_event_loop()
        coro = self.loop.create_server(lambda : ServerProtocol(self.process_data), host, port)
        self.serverInstance = self.loop.run_until_complete(coro)
        self.storage = Storage()
        self.parser = Request_Parser()
         
    def close_connection(self):
        self.serverInstance.close()
        self.loop.run_until_complete(self.serverInstance.wait_closed())
        self.loop.close()
        
    def process_data(self, data): 
        request = self.parser.parse_request(data.decode())
        if request is None:
            return Response.failure().encode()
        elif isinstance(request, Put_Request):
            self.storage.save_request(request)
        elif isinstance(request, Get_Request):
            result = self.storage.load_value_by_request(request)
            if result is None:
                return Response.success().encode()
            else :
                return Response.success(result).encode()
        return Response.success().encode()
    
        
class ServerProtocol(asyncio.Protocol):
    
    def __init__(self, process_data):
        self.process_data = process_data
    
    def connection_made(self, transport):
        self.transport = transport
 
    def data_received(self, data):
        response = self.process_data(data)
        self.transport.write(response)
 
    def connection_lost(self, exc):
        print('Connection ended')
        
      
    
def run_server(host, port):
    loop = asyncio.get_event_loop()
    server = Server(host, port)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close_connection()
        
if __name__ == '__main__':
    run_server("127.0.0.1",1818)
    
    