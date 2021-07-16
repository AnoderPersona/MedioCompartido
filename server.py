import socket
import time
import random
import os

#Funcion para recibir mensajes
def recibirMensaje(bS):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    return bytesAddressPair[0], bytesAddressPair[1]

#Funcion para codificar y enviar mensajes
def enviarMensaje(mensaje, direccion):
    bytesToSend = str.encode(mensaje)
    UDPServerSocket.sendto(bytesToSend, direccion)


localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 1024
msgFromServer       = "ACK" 
bytesToSend         = str.encode(msgFromServer)

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
print("Server conectado")

nombre = ''
idMensaje = 0
idCliente = 0
idClienteActual = 0
listaNombres = []

while(True):

    #Recibe mensajes
    print("Esperando mensaje")
    message, address = recibirMensaje(bufferSize)
    clientMsg = str(message)
    print("Mensaje recibido")

    #Si es la primera vez que se conecta el cliente, envía un conect y se le asigna un id
    if clientMsg == "b'conect'":
        print("Mensaje es connecting")
        idCliente += 1
        print("Id del cliente es:",idCliente)
        idClienteStr = str(idCliente)
        enviarMensaje(idClienteStr, address)
        listaNombres.append([])

    else:

        #Se revisa si es un número o no, en caso de ser un "done", luego se almacena el id
        if str(message)[4].isnumeric():
            idClienteActual = int(str(message)[4])

        else:
            idClienteActual = int(str(message)[6])

        #Se revisa si el cliente está listo, y si no, se continúa con el código
        if str(message)[:6] != "b'done":

            print("El mensaje del cliente {} es: {}".format(idCliente, clientMsg))

            #Genera probabilidad de pérdida y retraso del medio
            print("Generando probabilidad de perdida")
            pPerdida = random.randint(1,100)

            #Probabilidad de pérdida del 30%
            if pPerdida <= 30:
                tiempo = random.randint(2001, 3000)/1000
            else:
                tiempo = (random.randint(500,2000))/1000

            print("Se generó un restraso de {} ms por simulación del medio".format(tiempo))
            time.sleep(tiempo)

            #Si hay pérdida (Cuando el tiempo es mayor a 2000 ms), se notifica al cliente, y el cliente envía nuevamente los datos
            while tiempo >= 2:

                #Se genera de nuevo la probabilidad de pérdida y el retraso del medio
                pPerdida = random.randint(0,100)
                tiempo = (random.randint(500,3000))/1000
                time.sleep(tiempo)

                print("Se generó un restraso de {} ms por simulación del medio".format(tiempo))
                print("---Hubo una pérdida---")
                print("Enviando NAK")

                #Si hubo una pérdida, envía NAK al cliente y espera nuevo mensaje
                msgFromServer       = "NAK" 
                enviarMensaje(msgFromServer, address)

                print("Recibiendo mensaje perdido")

                #Recibe el mismo paquete desde el cliente
                message, address = recibirMensaje(bufferSize)

            #Para asegurarse de ingresar el mensaje correcto
            caracter = str(clientMsg[3])
            listaNombres[idClienteActual-1] += caracter
                
            print("Los nombres hasta ahora son: ",listaNombres)

            #Manda al cliente un ACK cuando acepta el paquete
            msgFromServer       = "ACK" 
            print("Enviando",msgFromServer)
            enviarMensaje(msgFromServer, address)
            print("---------")

        #Manda al cliente el nombre final
        else:
            print("Enviando nombre final:", listaNombres[idClienteActual-1])
            nombre = ''.join((listaNombres[idClienteActual-1]))
            enviarMensaje(nombre, address)
            idClienteActual = 0
