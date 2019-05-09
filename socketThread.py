#LUCAS DOMINGOS LEAO GOMES E KEVIN MIKEY
#GITHUB https://github.com/lucasdlg5/CriptografiaBranca

#py -2 .\socketThread.py
#Servidor TCP
import socket
from threading import Thread
import rsa
import time

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


def conexao(con,cli,guestPubKey):
    while True:
        msg = con.recv(1024)
        if not msg: break
        #Recebendo a chave publica para decifrar com a chave privada
        if (guestPubKey == ''):
            print('Guardando a chave publica do usuario')
            guestPubKey = msg
            pass
        #print('Chave publica do usuario: ', guestPubKey)
        print('Chave publica do usuario: ', myPriKey)
        print('Usuario : ')
        print (msg)
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
verifica_servidor = False
verifica_cliente = False
enviar_mensagem = False
resp = ''


def abre_servidor():
    verifica_servidor = False
    print ('Verificando Servidor')
    print ('Aguardando pela conexao de um usuario')
    con, cliente = tcp.accept()
    print ('Concetado por ', cliente)

    verifica_cliente = True
    t = Thread(target=conexao, args=(con,cliente,guestPubKey))
    t.start()
    if (verifica_cliente and resp == '1'):
        verifica_cliente = False
        time.sleep(2)
        abre_cliente(cliente[0])

def abre_cliente(SERVER):
    print('Abrindo Cliente')
    print ('Conectando ao IP : ', SERVER)
    destino = (SERVER, PORT)
    tcp2.connect(destino)
    if (verifica_servidor and resp == '2'):
        time.sleep(1)
        abre_servidor()
    envia_msg()


def envia_msg():
    print ('Para sair use CTRL+X\n')

    
    #msg = myPubKey
    msg = 'coxinha'

    print ('Enviando chave Publica:', msg)

    while msg <> '\x18':

        #tcp2.send (cifra(myPriKey,msg).encode())
        msg = cifra(myPubKey,msg)
        tcp2.send (msg)
        #tcp2.send (msg)

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
        verifica_servidor = True
        verifica_cliente = False
        enviar_mensagem = True
        print('Digite o IP de conexao: \n')
        abre_cliente(raw_input())

    elif verifica_servidor:
        verifica_servidor = False
        abre_servidor()

    elif enviar_mensagem:
        print('Entrou true para enviar msg')
        envia_msg()

    
    