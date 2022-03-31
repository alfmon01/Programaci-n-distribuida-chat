from multiprocessing.connection import Client
from random import random
from time import sleep

from multiprocessing.connection import Listener
from multiprocessing import Process

local_listener = (('127.0.0.1', 8001), b'secret password')

def client_listener():
    cl = Listener(address=local_listener[0], authkey=local_listener[1])
    while True:
        conn = cl.accept()
        print ('\nConexion aceptada del usuario', cl.last_accepted)       
        m = conn.recv()
        print (m)


if __name__ == '__main__':

    print ('Conectandose...')
    conn = Client(address=('127.0.0.1', 6000), authkey=b'secret password server')
    conn.send(local_listener)

    cl = Process(target=client_listener, args=())
    cl.start()
    
    connected = True
    while connected:
        value = input("Envia un mensaje (escribe 'quit' si quieres salir)")
        if value == 'quit':
            connected = False
        else:
            print ("Sigues dentro del chat")
            conn.send(f'{value}')
    conn.close()
    cl.terminate()
    print ("Acabas de salir del chat")
