import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, Entry, Button

def recibir_mensajes(cliente_socket):
    while True:
        mensaje = cliente_socket.recv(1024)
        mensaje_decodificado = mensaje.decode()
        mensaje_chat.insert(tk.END, mensaje_decodificado + "\n")

def enviar_mensaje():
    mensaje = mensaje_input.get()
    cliente_socket.send(mensaje.encode())
    mensaje_chat.insert(tk.END, "Tú: " + mensaje + "\n")
    mensaje_input.delete(0, tk.END)

def cliente():
    global cliente_socket
    host = "127.0.0.1"
    puerto = 12345

    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket.connect((host, puerto))

    thread_recibir = threading.Thread(target=recibir_mensajes, args=(cliente_socket,))
    thread_recibir.start()

#Configuracion de la interfaz gráfica
root = tk.Tk()
root.title("Cliente de Chat")
root.geometry("400x300")

#Area de mensajes recibidos
mensaje_chat = scrolledtext.ScrolledText(root, width=40, height=10, wrap=tk.WORD)
mensaje_chat.pack(padx=10, pady=10)

#Entrada de mensajes
mensaje_input = Entry(root, width=30)
mensaje_input.pack(padx=10, pady=5)

#Boton para enviar mensajes
boton_enviar = Button(root, text="Enviar", command=enviar_mensaje)
boton_enviar.pack(pady=5)

#Iniciar el cliente
cliente_thread = threading.Thread(target=cliente)
cliente_thread.start()

root.mainloop()
