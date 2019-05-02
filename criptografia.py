import rsa

def cifra(chave,mensagem):
    pub = rsa.PublicKey.load_pkcs1(chave, format='PEM')

    msgc = rsa.encrypt(mensagem, pub)

    return msgc

def decifra(chave_privada,msgc):
    chave_privada = rsa.PrivateKey.load_pkcs1(chave_privada, format='PEM')
    msg = rsa.decrypt(msgc, chave_privada)
    return msg

#############################Parte que cifra a mensagem########################################
#Nesta parte vc acessa a chave publica do seu amiguinho para cifrar a mensagem, onde depois que o seu aminguinho receber a mensagem
#ele possa descriptografar com a chhave privada dele...
arqnomepub ='.\criptografia\Pub.txt'

#Recebe a mensagem
msg = raw_input('Mensagem a ser cifrada: ')

arqnomemsg ='resposta.txt'

arq = open(arqnomepub,'r')
##carrego a chave
txt = ''
for linha in arq:
   txt = txt + linha

arq.close()


msgc = cifra(txt,msg)


arq = open(arqnomemsg,'w')
arq.write(msgc)
arq.close()

#############################Parte de descriptografia##########################################
#aq seria a 'leitura da sua chave privada para descriptografar, mas nao seria leitura de um arquivo...'
arqnomepri = 'E:\Arquivos\Documento\Fatec\criptografia\Pri.txt'#raw_input('Endereco da chave privada (c:\chaves\myPri.txt): ')

arqnomemsg = 'resposta.txt'#raw_input('Endereco e nome da mensagem a ser decifrada (c:\msg.txt): ')

arq = open(arqnomepri,'r')
##carrego a chave
txt = ''
for linha in arq:
   txt = txt + linha
arq.close()

arq = open(arqnomemsg,'r')
##carrego a msg cifrada
msgc = ''
for linha in arq:
   msgc = msgc + linha
arq.close()

print decifra(txt,msgc)