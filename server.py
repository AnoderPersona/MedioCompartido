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
idClienteActual = 0
listaNombres = []

while(True):

    print("Recibiendo mensaje")
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    clientMsg = str(message)
    print("Mensaje recibido")

    if clientMsg == "b'conect'":
        print("mensaje es connecting")
        idCliente += 1
        print("Id del cliente es:",idCliente)
        idClienteStr = str(idCliente)
        bytesToSend = str.encode(idClienteStr)
        UDPServerSocket.sendto(bytesToSend, address)
        listaNombres.append([])

    else:

        if str(message)[4].isnumeric():
            idClienteActual = int(str(message)[4])

        else:
            print(str(message))
            idClienteActual = int(str(message)[6])

        print(str(message)[:6])
        if str(message)[:6] != "b'done":

            print("El mensaje del cliente {} es: {}".format(idCliente, clientMsg))

            #Genera probabilidad de pérdida y retraso del medio
            print("Generando probabilidad de perdida")
            pPerdida = random.randint(1,100)
            print(pPerdida)

            if pPerdida <= 30:
                tiempo = random.randint(2001, 3000)/1000
            else:
                tiempo = (random.randint(500,2000))/1000

            print("Se generó un restraso de {} ms por simulación del medio".format(tiempo))
            time.sleep(tiempo)

            #Si hay pérdida (Cuando el tiempo es mayor a 2000 ms), se notifica al cliente, y el cliente envía nuevamente los datos
            while tiempo >= 2:
                print("hubo perdida")
                #Se genera de nuevo la probabilidad de pérdida y el retraso del medio
                pPerdida = random.randint(0,100)
                tiempo = (random.randint(500,3000))/1000
                time.sleep(tiempo)

                print("Se generó un restraso de {} ms por simulación del medio".format(tiempo))
                print("---Hubo una pérdida---")

                print("Enviando NAK")
                #Si hubo una pérdida, envía NAK al cliente y espera nuevo mensaje
                msgFromServer       = "NAK" 
                bytesToSend         = str.encode(msgFromServer)
                UDPServerSocket.sendto(bytesToSend, address)

                print("Recibiendo mensaje perdido")
                #Recibe el mismo paquete desde el cliente
                bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
                message = bytesAddressPair[0]
                address = bytesAddressPair[1]

            #Para asegurarse de ingresar el mensaje correcto
            print(clientMsg)
            caracter = str(clientMsg[3])
            listaNombres[idClienteActual-1] += caracter
                
            print("El nombre hasta ahora es: ",listaNombres[idClienteActual-1])#nombre)

            #Manda al cliente un ACK cuando acepta el paquete
            msgFromServer       = "ACK" #= "Datagram Acepted"
            bytesToSend         = str.encode(msgFromServer)
            print("Enviando",bytesToSend)
            UDPServerSocket.sendto(bytesToSend, address)
            print("---------")

        #Manda al cliente el nombre final
        else:
            print("Enviando nombre final:", listaNombres[idClienteActual-1])#nombre)
            nombre = ''.join((listaNombres[idClienteActual-1]))
            bytesToSend = str.encode(nombre)
            UDPServerSocket.sendto(bytesToSend, address)
            print("Link Available") 
            idClienteActual = 0
