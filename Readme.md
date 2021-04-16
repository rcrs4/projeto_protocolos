# Protocolo

Aqui temos a implementação do nosso protocolo.

## Requirements
para o funcionamento é necessário instalar os packages:
* pycryptodome
* getmac

## Como usar

1. por enquanto é preciso ter esses dois arquivos que são gerados pelo servidor ao chamar a função `generate_keys()`

      * server_private_key.pem
      * server_public_key.pem

2. após isso você deve abrir um programa instanciando o servidor e em outro o cliente 

3. Agora é necessário fazer o handshake entre eles usando as funções

### No client


```
client.connect_to_server(addrs = socket.gethostname(),port = 1234)
client.make_handshake()
```

### No server

```
server = protocolo.Server()
server.connect_to_client()
server.recv_packet()
```

## Funções

### Funções necessárias para usar o protocolo

   * `generate_keys()`       
      gera os arquivos necessários no passo 1         
   * `recv_packet()`     
      recebe o proximo pacote             
   * `send_msg()`       
      envia a mensagem (primeiro parâmetro) e o tipo dela (segundo parâmetro) em pacotes       
   * `connect_to_server()`        
      conecta ao servidor        
   * `make_handshake()`         
      faz o handshake com o servidor para autenticação           
   * `connection.close()`         
      fecha a conexão do cliente          
