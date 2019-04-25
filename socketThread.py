#Servidor TCP
import socket
from threading import Thread

def conexao(con,cli):
    while True:
        msg = con.recv(1024)
        if not msg: break
        print (msg)
    print ('Finalizando conexao do cliente', cli)
    con.close() 

#SERVER = raw_input()
#SERVER = '172.16.4.133'
SERVER = ''

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
while True:
    print ('Verificando Servidor')
    if verifica_servidor:
        print ('Aguardando pela conexao de um usuario')
        con, cliente = tcp.accept()
        SERVER = cliente
        print ('Concetado por ', cliente)
        t = Thread(target=conexao, args=(con,cliente,))
        t.start()
        verifica_servidor = False
        verifica_cliente = True

    print ('Verificando Cliente')
    if verifica_cliente:
        print ('Entre com o IP do servidor que deseja conectar:')
        #tcp.connect(raw_input())
        print ('Entrando com o IP : ', SERVER[0])
        destino = (SERVER[0], PORT)
        tcp2.connect(destino)
        enviar_mensagem = True

    if enviar_mensagem:
        #verifica_cliente = False
        print('entrou parte cliente')
        print ('Para sair use CTRL+X\n')
        print ('Digite uma mensagem para enviar\n')
        
        msg = raw_input()
        while msg <> '\x18':
            tcp2.send (msg.encode())
            print ('Digite uma mensagem para enviar\n')
            msg = raw_input()
        tcp.close()
    print ('Kevinho')
    
