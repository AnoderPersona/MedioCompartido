import socket
import random
import time
#
#msgFromClient       ="Using Link Client 1"
#

contador = 1
msgFromClient = ''
serverAddressPort   = ("127.0.0.1", 20001)
bufferSize          = 1024
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

bytesToSend = str.encode("conecting")
UDPClientSocket.sendto(bytesToSend, serverAddressPort)
msgFromServer = UDPClientSocket.recvfrom(bufferSize)
idCLiente = str(msgFromServer[0])[2]
print("ID de cliente es:", idCLiente)
print("Para salir ingrese: 'salir'")

while msgFromClient != "salir":
    print("------\n")

    msgFromClient = input("Cliente 1, ingrese su nombre carácter por carácter: ")
    msgFromClient = msgFromClient.lower()
    #
    if msgFromClient != "salir":
        bytesToSend         = str.encode(str(contador)+msgFromClient[0])

        # Send to server using created UDP socket
        print("Intentando enviar")

        # UDPClientSocket.sendto(bytesToSend, serverAddressPort)
        # msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        

        print(msgFromServer[0])

        while str(msgFromServer[0]) == "b'NAK'":
            print("Hubo una pérdida, intentando reenviar")
            UDPClientSocket.sendto(bytesToSend, serverAddressPort)
            msgFromServer = UDPClientSocket.recvfrom(bufferSize)

        #msg = "Message from Server {}".format(msgFromServer[0])
        print("Mensaje enviado con éxito")
        #print(msg)
        contador += 1

UDPClientSocket.sendto(str.encode("done"), serverAddressPort)
print("listoco")
msgFromServer = UDPClientSocket.recvfrom(bufferSize)
print("end")
nombre = str(msgFromServer[0])
nombre = nombre[1] + nombre[2].upper() + nombre[3:]
print("Su nombre es {}".format(nombre))