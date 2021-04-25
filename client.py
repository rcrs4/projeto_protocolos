import protocolo
import socket

def tiraespaco(string):
    aux = string.replace(" ", "_")
    return aux

def peganum():
    a = input()
    while(not a.isnumeric()):
        a = input("entrada invalida, digite um numero:\n")
    return a

def peganome():
    a = tiraespaco(input("digite um titulo para a sessao\n"))
    client.send_msg("", "F")
    nomes = client.recv_packet().split()
    tem = nomes.count(a)
    while(tem>0):
        a = tiraespaco(input("ja existe uma sessao com esse nome, digite outro\n"))
        tem = nomes.count(a)
    return a

def pegases(lista):
    retorno = tiraespaco(input())
    tem = lista.count(retorno)
    while(tem==0):
        retorno = tiraespaco(input("essa sessao nao existe, digite um nome valido\n"))
        tem = lista.count(retorno)
    return retorno

client = protocolo.Client()
client.connect_to_server(addrs=socket.gethostname(), port=1234)
client.make_handshake()

op = input("digite 1 para criar uma sessao de votacao\n2 para votar em uma sessao ja existente\n3 para checar seu resultado\nou digite 0 para sair\n")
while(op != '0'):
    
    if(op == '1'):
        tit = peganome()
        # print(tit)
        print("quantas opcoes a sessao tera?")
        quant = int(peganum())
        print("qual a quantidade de votos necessario para a vitoria?")
        total = peganum()
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
        print("sessoes em andamento:")
        client.send_msg("", "F")
        ses = client.recv_packet().split()
        for j in range(len(ses)):
            client.send_msg(ses[j],"F")
            ress = client.recv_packet()
            if(ress[0:9] != "vencedor "):
                print(ses[j])
        # sessao = input("em qual sessao voce deseja votar?\n")
        print("em qual sessao voce deseja votar?")
        sessao = pegases(ses)
        client.send_msg(sessao, "F")
        opcoes = client.recv_packet()
        if(opcoes[0:9] == "vencedor "):
            print("\nsessao ja finalizada\n")
        else:
            op = opcoes.split()
            print("suas opcoes sao:")
            for opc in range(len(op)):
                print(op[opc])
            # voto = input("qual sera seu voto?\n")
            print("qual sera seu voto?")
            voto = pegases(op)
            mensagem = sessao + " " + voto
            # print(mensagem)
            client.send_msg(mensagem, "V")
            if(client.recv_packet() == "OK"):
                print("seu voto foi computado com sucesso\n")
            else:
                print("ocorreu um erro na votacao\n")


    elif(op == '3'):
        print("sessoes finalizadas:")
        client.send_msg("", "F")
        ses = client.recv_packet().split()
        for j in range(len(ses)):
            client.send_msg(ses[j],"F")
            ress = client.recv_packet()
            if(ress[0:9] == "vencedor "):
                print(ses[j])    
        # sessao = input("qual sessao voce deseja saber o resultado?\n")
        print("qual sessao voce deseja saber o resultado?")
        sessao = pegases(ses)
        client.send_msg(sessao, "F")
        res = client.recv_packet()
        if(res[0:9] == "vencedor "):
            print("\n" + res,"\n")
        else:
            print(res)
            print("sessao ainda em andamento ou nao existente\n")

    else:
        print("\nopcao invalida, tente novamente\n")





    op = input("digite 1 para criar uma sessao de votacao\n2 para votar em uma sessao ja existente\n3 para checar seu resultado\nou digite 0 para sair\n")