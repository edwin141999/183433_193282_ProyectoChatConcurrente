import socket
import threading
from tkinter import *
import os, signal

usuario = ""
areaMessage = ""
message = ""

host = "127.0.0.1"
# host = "0.tcp.ngrok.io"
# host = "8.tcp.ngrok.io" #mio
port = 8000
# port = 10417
# port = 14834 #mio

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((host, port))


def enviarUsuario():
    mensaje = cliente.recv(1024).decode("utf8")
    print("mensaje:", mensaje)
    cliente.send(usuario.encode("utf8"))


def main():
    crearUsuario()


def crearUsuario():
    window = Tk()
    window.title("Bienvenido al Chat UP")
    window.geometry("300x100")

    titleLabel = Label(window, text="Chat UP")
    titleLabel.pack()

    chatLabel = Label(window, text="Introduce un usuario")
    chatLabel.pack()
    txtUsuario = Entry(window, width=20)
    txtUsuario.pack()

    txtAlertas = Label(window, text="")
    txtAlertas.pack()

    def entrarChat():
        global usuario
        if txtUsuario.get() == "":
            txtAlertas.configure(text="Escriba un nombre para identificarse")
        else:
            nombre = txtUsuario.get()
            usuario = nombre
            recibir_hilos = threading.Thread(target=enviarUsuario)
            recibir_hilos.start()
            window.destroy()
            chatConcurrente()

    btnEntrar = Button(window, text="Entrar", bg="red", fg="white", command=entrarChat)
    btnEntrar.pack()

    window.mainloop()


def chatConcurrente():
    window = Tk()
    window.title("Chat general")

    titleLabel = Label(window, text="CHAT GENERAL DE LA UP")
    titleLabel.pack()

    textArea = Text(window, height=20, width=40)
    textArea.pack()
    textArea.insert(INSERT, areaMessage)  # opcional

    txtMensaje = Entry(window, width=20)
    txtMensaje.pack()
    
    labelAlertas = Label(window, text="")
    labelAlertas.pack()

    def cerrarTerminal():
        os.kill(os.getpid(), signal.SIGTERM)

    def recibirMensaje():
        while True:
            try:
                mensaje = cliente.recv(1024).decode("utf8")
                textArea.configure(state="normal")
                textArea.insert(END, mensaje + "\n")
                textArea.configure(state="disabled")
            except OSError:
                break

    def enviarMensaje():
        if txtMensaje.get() == "":
            labelAlertas.configure(text="No puedes enviar mensajes vacios")
        else:
            global message
            labelAlertas.configure(text="")
            message = txtMensaje.get()
            message = f"{usuario}:{message}"
            txtMensaje.delete(0, END)
            cliente.send(bytes(message, "utf8"))
            textArea.configure(state="normal")
            textArea.insert(END, message + "\n")
            textArea.configure(state="disabled")

    btnEnviar = Button(
        window, text="Enviar", bg="blue", fg="white", command=enviarMensaje
    )
    btnEnviar.pack()
    btnSalir = Button(
        window, text="Salir", bg="green", fg="white", command=cerrarTerminal
    )
    btnSalir.pack()

    escribir_hilo = threading.Thread(target=recibirMensaje)
    escribir_hilo.start()
    window.mainloop()


if __name__ == "__main__":
    main()
