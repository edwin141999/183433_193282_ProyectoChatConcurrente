import socket
import threading

host = "127.0.0.1"
port = 8000

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((host,port))
servidor.listen()
print(f"Servidor corriendo en {host}:{port}")

clientes = []
usuarios = []

def transmisor(mensaje, _cliente):
    for cliente in clientes:
        if cliente != _cliente:
            cliente.send(mensaje)
            
def desconectar_cliente(cliente):
    index = clientes.index(cliente)
    usuario = usuarios[index]
    transmisor(f'ChatBot: {usuario} se desconecto'.encode('utf-8'),cliente)
    clientes.remove(cliente)
    usuarios.remove(usuario)
    cliente.close()
    print(f'{usuario} desconectado')
            
def receptor_mensajes(cliente):
    while True:
        try:
            mensaje = cliente.recv(1024)
            transmisor(mensaje,cliente)
        except:
            desconectar_cliente(cliente)
            break
        
def recibiendo_conexiones():
    while True:
        cliente, direccion = servidor.accept()
        
        cliente.send("@usuario".encode('utf-8'))
        usuario = cliente.recv(1024).decode('utf-8')
        
        clientes.append(cliente)
        usuarios.append(usuario)
        
        print(f'{usuario} se ha conectado con {str(direccion)}')
        
        mensaje = f"ChatBot: {usuario} ha entrado a la sala!".encode('utf-8')
        transmisor(mensaje,cliente)
        cliente.send('Conexion al servidor'.encode('utf-8'))
        
        thread = threading.Thread(target=receptor_mensajes,args=(cliente,))
        thread.start()

recibiendo_conexiones()            