from multiprocessing.connection import Listener, Client 
from multiprocessing import Process, Manager
from time import time 

import sys
import traceback


def nuevo_cliente(pid, clients):
    for client, client_info in clients.items():
        if not client == pid:
            with Client(address=client_info[0], authkey=client_info[1]) as conn:
                print("Nuevo cliente", client)
                conn.send((f'Acaba de entrar el nuevo cliente {client}'))
                conn.close()
            
                

    

def quitar_cliente(pid, clients):
    for client, client_info in clients.items():
       print("Cerrando la conexion del cliente", pid)
       with Client(address=client_info[0], authkey=client_info[1]) as conn:
            conn.send((f'El cliente {pid} ha salido del chat'))
    

def serve_client(conn, pid, clients):
    connected = True
    while connected:
        try:
            m = conn.recv()
            print(f'El mensaje recibido es {m} del cliente {pid}')
        except EOFError:
            print('connection abruptly closed by client')
            connected = False
            break
        if m == "quit":
            connected == False
            conn.close()
    del clients[pid]
    quitar_cliente(pid, clients)
    print(f'El cliente {pid} cierra su conexion')
            

def main(ip_address):
    with Listener(address = (ip_address, 6000), authkey = b'secret password server') as listener:
        print("Listener starting")
        
        m = Manager()
        clients = m.dict()
        
        while True:
            print ("Aceptando conexiones")
            try:
                conn = listener.accept()
                print("Conexion aceptada del cliente", listener.last_accepted)
                client_info = conn.recv()
                pid = listener.last_accepted
                clients[pid] = client_info
                
                
                nuevo_cliente(listener.last_accepted, clients)
                
                p = Process(target = serve_client, args = (conn, listener.last_accepted, clients))
                p.start()
            except Exception as e:
                traceback.print_exc()
        listener.close()
        print("End server")
        
        

if __name__ == '__main__':
    ip_address = '127.0.0.1'
    if len(sys.argv)>1:
        ip_address = sys.argv[1]
    main(ip_address)
    
