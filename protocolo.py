import socket


class Protocolo:
    def __init__(self):
        self.host = socket.gethostname()

    def make_header(self, option, msg_size):
        return bytes(option, 'utf-8') + msg_size.to_bytes(2, 'big')

    def make_packets(self, header, msg):
        total_packet = header + bytes(msg, 'utf-8')
        packet_size = 2048
        packets_list = [total_packet[i:i+packet_size] for i in range(0, len(total_packet), packet_size)]
        return packets_list

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
    
    def send_packet(self, client_socket, packets):
        for packet in packets:
            print(packet)
            sent = client_socket.send(packet)
            if sent == 0:
                raise RuntimeError("Socket connection broken")

    def recv_packet(self, client_socket):
        packet = client_socket.recv(2048)
        header = packet[:3]
        print(header)
        msg_len = int.from_bytes(header[1:3], 'big')
        msg_type = header[0]
        len_recv = len(packet[2:])
        msg_recv = [packet[2:].decode('utf-8')]
        print(len_recv, msg_len)
        while len_recv < msg_len:
            msg = client_socket.recv(2048)
            len_recv += len(msg)
            msg_recv.append(msg.decode('utf-8'))
        return ''.join(msg_recv)

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
    
    def send_packet(self, packets):
        for packet in packets:
            sent = self.connection.send(packet)
            if sent == 0:
                raise RuntimeError("Socket connection broken")
    
    def recv_packet(self):
        packet = self.connection.recv(2048)
        header = packet[:3]
        print(header)
        msg_len = int.from_bytes(header[1:3], 'big')
        msg_type = header[0]
        len_recv = len(packet[2:])
        msg_recv = [packet[2:].decode('utf-8')]
        while len_recv < msg_len:
            msg = self.connection.recv(2048)
            len_recv += len(msg)
            msg_recv.append(msg.decode('utf-8'))
        return ''.join(msg_recv)