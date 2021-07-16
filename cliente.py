import socket
import random
import time

contador = 1
msgFromClient = ''
serverAddressPort   = ("127.0.0.1", 20001)
bufferSize          = 1024
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

#Envía ping a servidor
bytesToSend = str.encode("conecting")
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

#Recibe respuesta del server
msgFromServer = UDPClientSocket.recvfrom(bufferSize)
idCLiente = str(msgFromServer[0])[2]
print("ID de cliente es:", idCLiente)
print("Para salir ingrese: 'salir'")

while msgFromClient != "salir":
    print("------\n")

    #Pide nombre a usuario
    msgFromClient = input("Cliente 1, ingrese su nombre carácter por carácter: ")
    msgFromClient = msgFromClient.lower()
    
    if msgFromClient != "salir":

        bytesToSend         = str.encode(str(contador)+msgFromClient[0])

        #Envía nombre a servidor
        print("Intentando enviar")
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)
        # msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        

        print(msgFromServer[0])

        #Si hay una pérdida, el servidor retorna NAK, pidiendo el paquete de nuevo
        while str(msgFromServer[0]) != "b'NAK'":
            print("Hubo una pérdida, intentando reenviar")
            UDPClientSocket.sendto(bytesToSend, serverAddressPort)
            msgFromServer = UDPClientSocket.recvfrom(bufferSize)

        print("Mensaje enviado con éxito")
        contador += 1

#Envia mensaje de terminado al server
UDPClientSocket.sendto(str.encode("done"), serverAddressPort)

#Recibe e imprime nombre final desde el servidor
msgFromServer = UDPClientSocket.recvfrom(bufferSize)
nombre = str(msgFromServer[0])
nombre = nombre[1] + nombre[2].upper() + nombre[3:]
print("Su nombre es {}".format(nombre))