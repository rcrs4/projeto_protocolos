import protocolo
import socket

client = protocolo.Client()
client.connect_to_server(addrs=socket.gethostname(), port=1234)
client.make_handshake()
client.send_msg("MelhorCampanho 3 jose arnaldo fernando", "C")
print(client.recv_packet())
client.send_msg("", "F")
print(client.recv_packet())
client.send_msg("MelhorCampanho", "F")
print(client.recv_packet())
client.send_msg("MelhorCampanho jose", "V")
print(client.recv_packet())
client.send_msg("MelhorCampanho jose", "V")
print(client.recv_packet())
client.send_msg("MelhorCampanho jose", "V")
print(client.recv_packet())
client.send_msg("MelhorCampanho", "F")
print(client.recv_packet())
while True:
    pass
#client.connection.close()
