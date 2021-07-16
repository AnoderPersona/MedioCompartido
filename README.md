# MedioCompartido
Trabajo para INFO239, comunicaciones. Enunciado dentro del repositorio.
-----
Se debe hacer un medio de comunicación, donde varios clientes estén conectados a la vez, y puedan enviar su nombre carácter por carácter.
-----
Archivos creados desde plantillas proporcionadas por el profesor a cargo.
-----
#Información del desarrollo

#Server
Para simular las pérdidas de 30% de probabilidad, se utiliza un random que vaya de 0 a 100, luego de esto hay una condición que si es menor que 30, existe una pérdida, y si no, no.

Para el retardo de mensaje, para simular el medio, se utiizó otro random, ya que si éste duraba más de 2000ms había una pérdida, lo junté con la probabilidad del 30%, cosa que, si el resultado del random era <= 30, el retardo era > 2000ms, pero si era mayor a 30, entonces el resultado era [500,2000]

Por cada pérdida, se imprime que sufrió una, se genera de nuevo la probabilidad de pérdida (ya que puede volver a ocurrir), se envía un NAK al cliente, y se espera a que reenvíe el paquete. Si se recibe bien, se envía un ACK.

Para soportar más de un cliente a la vez, a cada uno se le otorga una ID al conectarse con el server. Esto se logra cuando los clientes mandan su primer mensaje, éste siendo 'conect', además se añade una lista vacía a la lista donde se almacenan los nomrbes. Tener una ID diferente para cada clente permite guardar los carácteres de cada uno en una lista sin mezclarse.

Una vez que el cliente envía un "done", junta los carácteres dentro de la lista en un string, y se lo manda al cliente correspondiente.

#Clientes
Cada cliente empieza mandando un ping al server, y luego recibe su id proporcionado por él.

Se debe ingresar el nombre carácter por carácter, cada vez que se ingresa uno, se envía al servidor de la forma <Posición><carácter><idCliente>. Si el servidor retorna un NAK, se envía de nuevo el paquete automáticamente, e indica que se está enviando de nuevo.

Al ingresar "listo" o "salir" en la consola, se envía un "done" al servidor, recibe el nombre que le envía, y lo muestra en pantalla.
