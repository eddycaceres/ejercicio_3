import socket
import threading

#Diccionario para almacenar las conexiones de los clientes
clientes = {}

def manejar_cliente(cliente, direccion):
    while True:
        try:
            mensaje = cliente.recv(1024)
            if mensaje:
                #Retransmitir el mensaje a todos los clientes
                for socket_cliente in clientes:
                    if socket_cliente != cliente:
                        socket_cliente.send(f"{direccion}: {mensaje.decode()}".encode())
            else:
                #Si no hay datos recibidos, significa que el cliente se ha desconectado
                eliminar_cliente(cliente)
                break
        except:
            eliminar_cliente(cliente)
            break

def eliminar_cliente(cliente):
    del clientes[cliente]
    mensaje = "Cliente desconectado"
    broadcast(mensaje)

def broadcast(mensaje):
    for socket_cliente in clientes:
        socket_cliente.send(mensaje.encode())

def servidor():
    host = "127.0.0.1"
    puerto = 12345

    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.bind((host, puerto))
    servidor_socket.listen(5)

    print(f"Servidor escuchando en {host}:{puerto}")

    while True:
        cliente, direccion = servidor_socket.accept()
        clientes[cliente] = direccion
        print(f"Conexión entrante desde {direccion}")
        thread_cliente = threading.Thread(target=manejar_cliente, args=(cliente, direccion))
        thread_cliente.start()

if __name__ == "__main__":
    servidor()
