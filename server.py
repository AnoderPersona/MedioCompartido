import socket
import time
import random
import os

localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 1024
msgFromServer       = "ACK" 
bytesToSend         = str.encode(msgFromServer)

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
print("Link Available")

# Listen for incoming datagrams

nombre = ''
idMensaje = 0
idCliente = 0

while(True):


    #id = os.getpid()

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    print("Link bussy")

    idCliente += 1
    print("Id del cliente es:",idCliente)
    idClienteStr = str(idCliente)
    bytesToSend = str.encode(idClienteStr)
    UDPServerSocket.sendto(bytesToSend, address)    


    while str(message) != "b'done'":

        # bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        # message = bytesAddressPair[0]
        # address = bytesAddressPair[1]
        idMensaje += 1

        #Probabilidad de pérdida
    

    # #Si el mensaje no viene de donde se esperaba, le envía un mensaje de espera
    # if False:#bytesAddressPair[1] != address:
    #     UDPServerSocket.sendto(str.encode("Servidor ocupado, espere un poco"), bytesAddressPair[1])
    #     print("ocupado")

    #else:
        pPerdida = random.randint(0,100)
        print(pPerdida)

        clientMsg = format(message) 
        print("El mensaje del cliente es {}: {}".format(idCliente, clientMsg))
        
        #Retraso del medio
        tiempo = (random.randint(500,3000))/1000
        print("Se generó un restraso de {} ms por simulación del medio".format(tiempo))
        time.sleep(tiempo)

        #Si hay pérdida, se notifica al cliente, y el cliente envía nuevamente los datos
        while pPerdida <= 30:

            pPerdida = random.randint(0,100)
            tiempo = (random.randint(500,3000))/1000
            time.sleep(tiempo)
            print("Se generó un restraso de {} ms por simulación del medio".format(tiempo))

            #if idMensaje != clientMsg[2]:

            print("---Hubo una pérdida---")
            msgFromServer       = "NAK" 
            bytesToSend         = str.encode(msgFromServer)
            UDPServerSocket.sendto(bytesToSend, address)

            bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]

        #Para asegurarse de ingresar el mensaje correcto
        print(clientMsg[2], idMensaje)
        if int(clientMsg[2]) == idMensaje:
            nombre += str(clientMsg[3])
            
        print("El nombre es: ",nombre)
        msgFromServer       = "ACK" #= "Datagram Acepted"
        bytesToSend         = str.encode(msgFromServer)
        UDPServerSocket.sendto(bytesToSend, address)
        print("---------")

        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        idMensaje += 1
        print("Link bussy")

    bytesToSend = str.encode(nombre)
    UDPServerSocket.sendto(bytesToSend, address)
    print("Link Available") 