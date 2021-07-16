import socket
import random
import time

contador = 1
msgFromClient = ''
serverAddressPort   = ("127.0.0.1", 20001)
bufferSize          = 1024
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

parche = 0

print("Enviando ping al servidor")
#Envía ping a servidor
bytesToSend = str.encode("conect")
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

print("Recibiendo respuesta del servidor")
#Recibe respuesta del server
msgFromServer = UDPClientSocket.recvfrom(bufferSize)
idCLiente = str(msgFromServer[0])[2]
print("ID de cliente es:", idCLiente)
print("Para salir ingrese: 'salir'")

while msgFromClient != "salir" and msgFromClient != "listo":
    print("------\n")

    #Pide nombre a usuario
    msgFromClient = input("Cliente 1, ingrese su nombre carácter por carácter: ")
    msgFromClient = msgFromClient.lower()
    
    if msgFromClient != "salir" and msgFromClient != "listo":

        bytesToSend         = str.encode(str(contador)+msgFromClient[0]+idCLiente)

        #Envía nombre a servidor
        print("Intentando enviar", msgFromClient)
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)
        print("Recibiendo respuesta")
        msgFromServer = UDPClientSocket.recvfrom(bufferSize) 
        
        #Si hay una pérdida, el servidor retorna NAK, pidiendo el paquete de nuevo
        while str(msgFromServer[0]) == "b'NAK'":
            print("Hubo una pérdida, intentando reenviar")
            UDPClientSocket.sendto(bytesToSend, serverAddressPort)
            msgFromServer = UDPClientSocket.recvfrom(bufferSize)

        #print(msgFromServer)
        if str(msgFromServer[0]) == "b'ACK'":
            print("Mensaje enviado con éxito")
            contador += 1

        else:
            print(str(msgFromServer[0])[2:-1])

#Envia mensaje de terminado al server
UDPClientSocket.sendto(str.encode("done" + idCLiente), serverAddressPort)

#Recibe e imprime nombre final desde el servidor
msgFromServer = UDPClientSocket.recvfrom(bufferSize)
nombre = str(msgFromServer[0])
nombre = nombre[1] + nombre[2].upper() + nombre[3:]
print("Su nombre es {}".format(nombre))