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

nombre = ''
idMensaje = 0
idCliente = 0

#Recibe connecting
bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
message = bytesAddressPair[0]
address = bytesAddressPair[1]

# idCliente += 1
# print("Id del cliente es:",idCliente)
# idClienteStr = str(idCliente)
# bytesToSend = str.encode(idClienteStr)

#Envía id del cliente
UDPServerSocket.sendto(bytesToSend, address) 

while(True):

    print("Link bussy")

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    idMensaje += 1    

    while str(message) != "b'done'":

        #Recibe mensaje
        print("a")
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        idMensaje += 1    

        clientMsg = format(message) 
        print("El mensaje del cliente es {}: {}".format(idCliente, clientMsg))
        

        #Genera probabilidad de pérdida y retraso del medio
        pPerdida = random.randint(1,100)
        print(pPerdida)

        if pPerdida <= 30:
            tiempo = random.randint(2001, 3000)/1000
        else:
            tiempo = (random.randint(500,2000))/1000

        print("Se generó un restraso de {} ms por simulación del medio".format(tiempo))
        time.sleep(tiempo)

        #Si hay pérdida (Cuando el tiempo es mayor a 2000 ms), se notifica al cliente, y el cliente envía nuevamente los datos
        while timpo <= 2:

            #Se genera de nuevo la probabilidad de pérdida y el retraso del medio
            pPerdida = random.randint(0,100)
            tiempo = (random.randint(500,3000))/1000
            time.sleep(tiempo)

            print("Se generó un restraso de {} ms por simulación del medio".format(tiempo))
            print("---Hubo una pérdida---")

            #Si hubo una pérdida, envía NAK al cliente y espera nuevo mensaje
            msgFromServer       = "NAK" 
            bytesToSend         = str.encode(msgFromServer)
            UDPServerSocket.sendto(bytesToSend, address)

            #Recibe el mismo paquete desde el cliente
            bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]

        #Para asegurarse de ingresar el mensaje correcto
        print(clientMsg[2], idMensaje)
        if int(clientMsg[2]) == idMensaje:
            nombre += str(clientMsg[3])
            
        
        print("El nombre es: ",nombre)

        #Manda al cliente un ACK cuando acepta el paquete
        msgFromServer       = "ACK" #= "Datagram Acepted"
        bytesToSend         = str.encode(msgFromServer)
        UDPServerSocket.sendto(bytesToSend, address)
        print("---------")

        # #Recibe mensaje
        # bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        # message = bytesAddressPair[0]
        # address = bytesAddressPair[1]
        # idMensaje += 1
        # print("Link bussy")

    #Manda al cliente el nombre final
    bytesToSend = str.encode(nombre)
    UDPServerSocket.sendto(bytesToSend, address)
    print("Link Available") 