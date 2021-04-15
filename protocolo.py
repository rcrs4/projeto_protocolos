import socket
import uuid
import hashlib
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA384
import binascii

class Protocolo:
    def __init__(self):
        self.host = socket.gethostname()

    def make_header(self, option, msg_size):
        return bytes(option, 'utf-8') + msg_size.to_bytes(2, 'big')

    def make_packets(self, header, msg):
        total_packet = header + bytes(msg, 'utf-8')
        packet_size = 4080
        packets_list = [total_packet[i:i+packet_size] for i in range(0, len(total_packet), packet_size)]
        return packets_list

    def send_msg(self, msg, option, socket=None):
        header = self.make_header(option, len(msg))
        packets = self.make_packets(header, msg)
        for packet in packets:
            if(socket):
                self.send_packet(socket, packet)
            else:
                self.send_packet(packet)

    def generate_mac(self, msg, key):
        mac_msg = msg+key
        return hashlib.md5(mac_msg).digest()
    
    def compare_mac(self, msg, key, hash_msg):
        return self.generate_mac(msg, key) == hash_msg
    
    def encrypt_rsa(self, msg):
        pubKey = RSA.importKey(open("server_public_key.pem", "rb").read())
        
        encryptor = PKCS1_OAEP.new(pubKey)
        encrypted = encryptor.encrypt(msg)
        
        return encrypted
    
    def decrypt_rsa(self, msg):
        privKey = RSA.importKey(open("server_private_key.pem", "rb").read())
        
        decryptor = PKCS1_OAEP.new(privKey)
        decrypted = decryptor.decrypt(msg)
        
        return decrypted
    
    def sign_msg(self, msg):
        digest = SHA384.new()
        digest.update(msg)

        privKey = RSA.importKey(open("server_private_key.pem", "rb").read())
        
        signer = pkcs1_15.new(privKey)
        signed = signer.sign(digest)

        return signed

    
    def verify_msg(self, hash_msg, msg):
        pubKey = RSA.importKey(open("server_public_key.pem", "rb").read())

        verifier = pkcs1_15.new(pubKey)
        hash_verify = SHA384.new()
        hash_verify.update(msg)
        try:
            verifier.verify(hash_verify, hash_msg)
        except ValueError:
            return False
        else:
            return True
    
class Server(Protocolo):
    def __init__(self, address = None, port=1234):
        super().__init__()
        if address == None:
            address = self.host
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.bind((address, port))
        self.connection.listen(5)
        self.client_mac_key = None
        self.func_options = {ord("H"):self.hello_case, ord("F"):self.fetch_case, ord("C"):self.create_case}
        self.client_socket = None

    def verify_client_authentication(self, msg, hash):
        return self.compare_mac(msg, self.client_mac_key, hash)
    
    def generate_keys(self):
        keyPair = RSA.generate(3072)
        pubKey = keyPair.publickey()
        pubKeyPEM = pubKey.exportKey(format='PEM')
        privKeyPEM = keyPair.exportKey(format='PEM')
        with open('server_public_key.pem', 'wb') as pub_file:
            pub_file.write(pubKeyPEM)
        
        with open('server_private_key.pem', 'wb') as priv_file:
            priv_file.write(privKeyPEM)

    def connect_to_client(self):
        client_socket, _ = self.connection.accept()
        self.client_socket = client_socket
        return client_socket
    
    def send_packet(self, client_socket, packet):
        hash = self.sign_msg(packet)
        sent = client_socket.send(packet+hash)
        if sent == 0:
            raise RuntimeError("Socket connection broken")
    
    def hello_case(self, msgs, hashs):
        if msgs[0][3:8] == b"HELLO":
            self.client_mac_key = msgs[0][8:]
        else:
            self.close_connection()
            return False

        for msg, hash in zip(msgs, hashs):
            if(self.verify_client_authentication(msg, hash) == False):
                self.close_connection()
                return False
        self.send_msg("HELLO", "H", self.client_socket)
        return True

    def fetch_case(self, msgs, hashs):
        for msg, hash in zip(msgs, hashs):
            if(self.verify_client_authentication(msg, hash) == False):
                self.close_connection()
                return False

    def create_case(self, msgs, hashs):
        for msg, hash in zip(msgs, hashs):
            if(self.verify_client_authentication(msg, hash) == False):
                self.close_connection()
                return False

    def recv_packet(self, client_socket=None):
        if(client_socket == None):
            client_socket = self.client_socket
        packet = client_socket.recv(4096)
        packet = self.decrypt_rsa(packet)
        header = packet[:3]
        msg_len = int.from_bytes(header[1:3], 'big')
        msg_type = header[0]
        len_recv = len(packet[3:-16])
        msg_recv = [packet[:-16]]
        hashs = [packet[-16:]]
        while len_recv < msg_len:
            msg = client_socket.recv(4096)
            mag = self.decrypt_rsa(msg)
            len_recv += len(msg[:-16])
            msg_recv.append(msg[:-16])
            hashs.append(msg[-16:])
        return self.func_options[msg_type](msg_recv, hashs)

    def close_connection(self):
        self.client_socket.close_connection()
        self.client_socket = None

    def close_server(self):
        self.connection.close()

class Client(Protocolo):
    def __init__(self):
        super().__init__()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mac_key = None

    def verify_server_authentication(self, msg, hash_msg):
        return self.verify_msg(hash_msg, msg)
    
    def connect_to_server(self, addrs=None, port=1234):
        if addrs == None:
            addrs = self.host
        self.connection.connect((addrs, port))
    
    def generate_mac_key(self):
        mac_key = uuid.uuid1()
        self.mac_key = str(mac_key).encode()
        return mac_key
    
    def send_packet(self, packet):
        mac = self.generate_mac(packet, self.mac_key)
        msg = self.encrypt_rsa(packet+mac)
        sent = self.connection.send(msg)
        if sent == 0:
            raise RuntimeError("Socket connection broken")
    
    def recv_packet(self):
        packet = self.connection.recv(4096)
        header = packet[:3]
        msg_len = int.from_bytes(header[1:3], 'big')
        msg_type = header[0]
        len_recv = msg_len+3
        full_msg = packet[:len_recv]
        msg_recv = packet[3:len_recv].decode('utf-8')
        hash = packet[len_recv:]
        if(self.verify_server_authentication(full_msg, hash) == False):
            return ''
        return msg_recv
    
    def make_handshake(self):
        msg = "HELLO"
        self.send_msg(msg+self.mac_key.decode(), "H")
        msg_recv = self.recv_packet()
        if msg_recv != "HELLO":
            self.close_connection()
            return False
        return True
            
    def close_connection(self):
        self.connection.close()