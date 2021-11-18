import socket
import threading
from tkinter import *
import sys

# usuario = input('Introduce un usuario: ')
usuario = ""
areaMessage = ""
message = ""

host = "127.0.0.1"
port = 8000

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((host, port))


def enviar_nombre():
    global areaMessage
    mensaje = cliente.recv(1024).decode("utf8")
    print("mensaje:", mensaje)
    cliente.send(usuario.encode("utf8"))
    # while True:
    #     try:
    #         mensaje = cliente.recv(1024).decode("utf8")
    #         if mensaje == "@usuario":
    #             cliente.send(usuario.encode("utf8"))
    #             print('usuario:',usuario)
    #         else:
    #             print(mensaje + " -> ver")
    #             areaMessage = mensaje
    #     except:
    #         print("Un error ha ocurrido")
    #         cliente.close()
    #         break


def escribir_mensajes():
    # while True:
    # mensaje = f"{usuario}:{input('')}"
    mensaje = f"{usuario}:{message}"
    cliente.send(mensaje.encode("utf-8"))


def main():
    ventana()


def ventana():
    window = Tk()
    window.title("Bienvenido al Chat UP")
    window.geometry("300x100")

    titleLabel = Label(window, text="Chat UP")
    titleLabel.pack()

    chatLabel = Label(window, text="Introduce un usuario")
    chatLabel.pack()
    txtUsuario = Entry(window, width=20)
    txtUsuario.pack()
    # txtUsuario.focus()

    def enviar():
        global usuario
        nombre = txtUsuario.get()
        usuario = nombre
        recibir_hilos = threading.Thread(target=enviar_nombre)
        recibir_hilos.start()
        window.destroy()
        ventana2()

    btnEntrar = Button(window, text="Entrar", bg="red", fg="white", command=enviar)
    btnEntrar.pack()

    window.mainloop()


def ventana2():
    window = Tk()
    window.title("Chat general")

    titleLabel = Label(window, text="CHAT GENERAL DE LA UP")
    titleLabel.pack()

    textArea = Text(window, height=20, width=40)
    textArea.pack()
    textArea.insert(INSERT, areaMessage)  # opcional

    txtMensaje = Entry(window, width=20)
    txtMensaje.pack()

    def cerrarTerminal():
        window.destroy()

    def recibir():
        while True:
            try:
                mensaje = cliente.recv(1024).decode("utf8")
                # if mensaje == "@usuario":
                #     # cliente.send(usuario.encode("utf-8"))
                #     print('entroif')
                # else:
                #     print(mensaje + " -> else")
                # ver = f"{usuario}:{mensaje}"
                # ver = f"{cliente}:{mensaje}"
                # print('cliente:',cliente)
                # print('usuario:',usuario)
                # textArea.insert(END, areaMessage + "\n")  # opcional
                # textArea.insert(END, ver)
                textArea.insert(END, mensaje + "\n")
            except OSError:
                break

    def enviarMensaje():
        global message
        message = txtMensaje.get()
        message = f"{usuario}:{message}"
        txtMensaje.delete(0, END)
        # print('cliente:',cliente)
        # print('usuario:',usuario)
        # print('message:',message)
        # textArea.insert(INSERT, areaMessage + "\n")
        cliente.send(bytes(message, "utf8"))
        # ver = f"{usuario}:{message}"
        # textArea.insert(INSERT, ver + "\n")
        textArea.insert(END, message + "\n")

    btnEnviar = Button(
        window, text="Enviar", bg="blue", fg="white", command=enviarMensaje
    )
    btnEnviar.pack()
    btnImagenes = Button(window, text="Archivos", bg="red", fg="white")
    btnImagenes.pack()
    btnSalir = Button(
        window, text="Salir", bg="green", fg="white", command=cerrarTerminal
    )
    btnSalir.pack()

    escribir_hilo = threading.Thread(target=recibir)
    escribir_hilo.start()
    window.mainloop()


if __name__ == "__main__":
    main()
