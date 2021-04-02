import socket


class Protocolo:
    def __init__(self):
        self.host = socket.gethostname()

    def make_header(self):
        raise NotImplementedError

    def make_packet(self):
        raise NotImplementedError

    def send_packet(self):
        raise NotImplementedError

    def recv_packet(self):
        raise NotImplementedError

    def generate_mac(self):
        raise NotImplementedError
    
    def compare_mac(self):
        raise NotImplementedError
    
    def encript_rsa(self):
        raise NotImplementedError
    
    def decript_rsa(self):
        raise NotImplementedError
    
class Server(Protocolo):
    def __init__(self, address = None, port=1234):
        super().__init__()
        if address == None:
            address = self.host
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.bind((address, port))
        self.connection.listen(5)

    def verify_client_authentication(self):
        raise NotImplementedError
    
    def generate_keys(self):
        raise NotImplementedError
    
    def connect_to_client(self):
        client_socket = self.connection.accept()
        return client_socket
    
    def send_packet(self, client_socket, packet):
        client_socket.send(packet)

    def recv_packet(self, client_socket):
        return client_socket.recv(2048)

class Client(Protocolo):
    def __init__(self):
        super().__init__()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def verify_server_authentication(self):
        raise NotImplementedError
    
    def connect_to_server(self, addrs=None, port=1234):
        if addrs == None:
            addrs = self.host
        self.connection.connect((addrs, port))
    
    def generate_mac_key(self):
        raise NotImplementedError
    
    def send_packet(self, packet):
        self.connection.send(packet)
    
    def recv_packet(self):
        return self.connection.recv(2048)