Multi-line comments are here!

You can now comment on multiple lines. Just click and drag on the  button.

Demonstrating selecting multiple lines for commenting

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
      
## Autenticação
   A autenticação do servidor é feito pela assinatura no uso da função `sign_msg`, toda vez que o servidor enviar mensagens, e é verificada no cliente com a função `verify_msg` toda vez que é chamada a função `recv_packet` para receber pacotes.

   Já a autenticação do cliente se da pela função `compare_mac`, que compara se a assinatura da mensagem foi realmente feita pela chave única do cliente, gerada na função `generate_mac`
   
   
## Confidencialidade

   A confidencialidade dos dados se da pela encriptação dos dados enviados pelo cliente para o servidor graças às funções `encrypt_rsa`, que é chamada quando o cliente vai enviar uma mensagem e é decriptada pela função  `decrypt_rsa` sempre que o servidor receber mensagens.


