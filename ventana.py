import socket
import threading
from tkinter import *

# usuario = input('Introduce un usuario: ')
usuario = ''

host = "127.0.0.1"
port = 8000

cliente = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
cliente.connect((host,port))

def recibir_mensajes():
    while True:
        try:
            mensaje = cliente.recv(1024).decode('utf-8')
            if mensaje == "@usuario":
                cliente.send(usuario.encode('utf-8'))
            else:
                print(mensaje)
        except:
            print("Un error ha ocurrido")
            cliente.close()
            break

def escribir_mensajes():
    while True:
        mensaje = f"{usuario}:{input('')}"
        cliente.send(mensaje.encode('utf-8'))

def main():
    ventana()

def ventana():
    window = Tk()
    window.title("Bienvenido al Chat UP")
    window.geometry('330x200')
    
    titleLabel = Label(window,text="Chat UP")
    titleLabel.grid(row=0,column=0)
    
    chatLabel = Label(window,text="Introduce un usuario")
    chatLabel.grid(row=1,column=0)
    txtUsuario = Entry(window,width=20)
    txtUsuario.grid(row=1,column=1)
    txtUsuario.focus()
    
    def enviar():
        global usuario
        nombre = txtUsuario.get()
        usuario = nombre
        recibir_hilos = threading.Thread(target=recibir_mensajes)
        recibir_hilos.start()
        window.destroy()
        ventana2()
        # escribir_hilo = threading.Thread(target=escribir_mensajes)
        # escribir_hilo.start()
    
    btnEntrar = Button(window,text='Entrar', bg='red',fg='white',command=enviar)
    btnEntrar.grid(row=1,column=2)
    window.mainloop()
    
def ventana2():
    window = Tk()
    window.title('Chat general')
    window.geometry('500x500')
    window.grid()
    
    titleLabel = Label(window,text='CHAT GENERAL DE LA UP')
    titleLabel.grid(row=0,column=0,columnspan=3)
    
    textArea = Text(window,height=20,width=40, state=DISABLED)
    textArea.grid(row=1,column=0,columnspan=2)
    
    txtMensaje = Entry(window,width=20)
    txtMensaje.grid(row=2,column=0,columnspan=2,)
    
    btnEnviar = Button(window,text='Enviar',bg='blue',fg="white")
    btnEnviar.grid(row=3,column=0)
    btnImagenes = Button(window,text='Archivos',bg='red',fg='white')
    btnImagenes.grid(row=3,column=1)
    btnSalir = Button(window,text='Salir',bg='green',fg="white")
    btnSalir.grid(row=3,column=2)
    
    window.mainloop()


if __name__ == '__main__':
    main()