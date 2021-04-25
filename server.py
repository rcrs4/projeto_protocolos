import protocolo

server = protocolo.Server()

msg = b"OK"
while True:
    server.connect_to_client()
    print("client connected")
    status = True
    while status != False:
        status = server.recv_packet()
