#py -2 .\socketThread.py
#Servidor TCP
import socket
from threading import Thread
import rsa

guestPubKey = ''
arqnomepub = '.\Pub.txt'
arqnomepri = '.\Pri.txt'
## LEITURA DE CHAVE PUBLICA
arq = open(arqnomepub,'r')
##carrego a chave
myPubKey = ''
for linha in arq:
   myPubKey = myPubKey + linha

arq.close()

SERVER = ''

## LEITURA DE CHAVE PRIVADA
arq = open(arqnomepri,'r')
##carrego a chave
myPriKey = ''
for linha in arq:
   myPriKey = myPriKey + linha
arq.close()


def cifra(chave,mensagem):
    pub = rsa.PublicKey.load_pkcs1(chave, format='PEM')

    msgc = rsa.encrypt(mensagem, pub)

    return msgc

def decifra(chave_privada,msgc):
    chave_privada = rsa.PrivateKey.load_pkcs1(chave_privada, format='PEM')
    msg = rsa.decrypt(msgc, chave_privada)
    return msg    


def conexao(con,cli):
    while True:
        msg = con.recv(1024)
        if not msg: break
        #Recebendo a chave publica para decifrar com a chave privada
        if (pubKey == ''):
            pubKey = msg
        #print('Usuario : ', SERVER[0])
        print('Usuario : ')
        print (decifra(myPriKey,msg))
    print ('Finalizando conexao do cliente', cli)
    con.close() 
#############################Parte que cifra a mensagem########################################



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

    verifica_cliente = True
    t = Thread(target=conexao, args=(con,cliente,))
    t.start()
    resp = 1
    abre_cliente()


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
    print ('Para sair use CTRL+X\n')

    print ('Enviando chave Privada:')
    
    #msg = raw_input()
    msg = myPubKey
    while msg <> '\x18':

        tcp2.send (cifra(myPubKey,msg).encode())
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

    
    