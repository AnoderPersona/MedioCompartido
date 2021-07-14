import socket
import random
import time
#
#msgFromClient       ="Using Link Client 1"
#
msgFromClient = input("Cliente 1, Ingrese algo: ")
#
bytesToSend         = str.encode(msgFromClient)
serverAddressPort   = ("127.0.0.1", 20001)
bufferSize          = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket
print("Intentando enviar")

#Retraso del medio
tiempo = (random.randint(500,3000))/1000
print("Se generó un restraso de {} ms por simulación del medio".format(tiempo))
time.sleep(tiempo)
#

UDPClientSocket.sendto(bytesToSend, serverAddressPort)
msgFromServer = UDPClientSocket.recvfrom(bufferSize)
msg = "Message from Server {}".format(msgFromServer[0])
print(msg)