#py -2 .\socketThread.py
#Servidor TCP
import socket
from threading import Thread

#SERVER = raw_input()
#SERVER = '172.16.4.133'
SERVER = ''
def conexao(con,cli):
    while True:
        msg = con.recv(1024)
        if not msg: break

        #print('Usuario : ', SERVER[0])
        print('Usuario : ')
        print (msg)
    print ('Finalizando conexao do cliente', cli)
    con.close() 


# Endereco IP do Servidor

# Porta que o Servidor vai escutar
PORT = 5002
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (SERVER, PORT)

tcp.bind(orig)
tcp.listen(1)
verifica_servidor = True
verifica_cliente = False
enviar_mensagem = False
resp = ''

def abre_servidor():
    print ('Verificando Servidor')
    print ('Aguardando pela conexao de um usuario')
    con, cliente = tcp.accept()
    SERVER = cliente
    print ('Concetado por ', cliente)
    t = Thread(target=conexao, args=(con,cliente,))
    t.start()


def abre_cliente():
    print('Abrindo Cliente')
    if (resp == 1):
        print ('\n\nConectando ao IP : ', SERVER[0])
        destino = (SERVER[0], PORT)
        tcp2.connect(destino)
    else:
        print('Digite o IP de conexao: \n')
        SERVER = raw_input()
        destino = (SERVER, PORT)
        tcp2.connect(destino)

def envia_msg():
    #verifica_cliente = False
    print ('Para sair use CTRL+X\n')
    print ('Eu digo:')
    
    msg = raw_input()
    while msg <> '\x18':
        tcp2.send (msg.encode())
        print ('Eu digo:')
        msg = raw_input()
    tcp.close()

while True:

    if (resp == ''):
        print('1 - Abrir Servidor\n2 - Conectar')
        resp = raw_input()
        if (resp == '1'):
            print('Entrou 1')
            verifica_servidor = True
        elif (resp == '2'):
            print('Entrou 2')
            verifica_cliente = True

    if verifica_cliente:
        abre_cliente()
        verifica_cliente = False
        enviar_mensagem = True

    elif verifica_servidor:
        abre_servidor()
        verifica_servidor = False

    elif enviar_mensagem:
        envia_msg()

    
    