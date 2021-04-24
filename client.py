import protocolo
import socket

def tiraespaco(string):
    aux = string.replace(" ", "_")
    return aux




client = protocolo.Client()
client.connect_to_server(addrs=socket.gethostname(), port=1234)
client.make_handshake()

op = input("digite 1 para criar uma sessao de votacao\n2 para votar em uma sessao ja existente\n3 para checar seu resultado\nou digite 0 para sair\n")
while(op != '0'):
    
    if(op == '1'):
        tit = tiraespaco(input("digite um titulo para a sessao\n"))
        print(tit)
        quant = int(input("quantas opcoes a sessao tera?\n"))
        total = input("qual a quantidade de votos para a reuniao acabar?\n")
        opcoes = ""
        i=0
        quanto =int(quant)
        while(i<quanto):
            print("digite o nome da opcao",i+1)
            entrada = tiraespaco(input())
            if(entrada == "vencedor" and i==0):
                print("opcao invalida tente novamente")
                i-=1
            else:
                opcoes = opcoes + " " + entrada
            i+=1

        mensagem = tit + " " + total + opcoes
        client.send_msg(mensagem, "C")
        if(client.recv_packet() == "OK"):
            print("sessao criada com sucesso\n")
        else:
            print("ocorreu um erro na criacao da sessao\n")
        # print(client.recv_packet())

    elif(op == '2'):
        print("sessoes existentes:")
        client.send_msg("", "F")
        ses = client.recv_packet().split()
        for j in range(len(ses)):
            print(ses[j])
        sessao = input("em qual sessao voce deseja votar?\n")
        client.send_msg(sessao, "F")
        opcoes = client.recv_packet()
        if(opcoes[0:9] == "vencedor "):
            print("\nsessao ja finalizada\n")
        else:
            op = opcoes.split()
            print("suas opcoes sao:")
            for opc in range(len(op)):
                print(op[opc])
            voto = input("qual sera seu voto?\n")
            mensagem = sessao + " " + voto
            # print(mensagem)
            client.send_msg(mensagem, "V")
            if(client.recv_packet() == "OK"):
                print("seu voto foi computado com sucesso\n")
            else:
                print("ocorreu um erro na votacao\n")


    elif(op == '3'):
        print("sessoes existentes:")
        client.send_msg("", "F")
        ses = client.recv_packet().split()
        for j in range(len(ses)):
            print(ses[j])    
        sessao = input("qual sessao voce deseja saber o resultado?\n")
        client.send_msg(sessao, "F")
        res = client.recv_packet()
        if(res[0:9] == "vencedor "):
            print("\n" + res,"\n")
        else:
            print("sessao ainda em andamento ou nao existente\n")

    else:
        print("\nopcao invalida, tente novamente\n")





    op = input("digite 1 para criar uma sessao de votacao\n2 para votar em uma sessao ja existente\n3 para checar seu resultado\nou digite 0 para sair\n")






# client.send_msg("MelhorCampanho 3 jose arnaldo fernando", "C")
# print(client.recv_packet())
# client.send_msg("", "F")
# print(client.recv_packet())
# client.send_msg("MelhorCampanho", "F")
# print(client.recv_packet())
# client.send_msg("MelhorCampanho jose", "V")
# print(client.recv_packet())
# client.send_msg("MelhorCampanho jose", "V")
# print(client.recv_packet())
# client.send_msg("MelhorCampanho jose", "V")
# print(client.recv_packet())
# client.send_msg("MelhorCampanho", "F")
# print(client.recv_packet())
# while True:
#     pass
#client.connection.close()
