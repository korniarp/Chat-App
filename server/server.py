from socket import AF_INET,socket,SOCK_STREAM
from threading import Thread
import time
import sys
from person import Person
#GLOBAL CONSTANTS
#HOST = '192.168.209.1'
#HOST = '10.196.2.83'
HOST = 'localhost'
PORT = 50
ADDR = (HOST,PORT)

MAX_CONNECTIONS=10
BUFSIZ = 512

#GLOBAL VARIABLES
persons = []
SERVER= socket(AF_INET,SOCK_STREAM)
SERVER.bind(ADDR) #set up server


def broadcast(msg,name):
    """
    send new messages to all clients
    :param msg: bytes["utf8"]
    :param name: str
    :return:
    """
    for person in persons:
        client = person.client
        client.send(bytes(name+": ","utf8")+msg)


def client_communication(person):
    """
      Thread to handle all messages from client
      :param person : Person
      :return :None
      """

    client=person.client
    #addr=person.addr

    #get persons name
    name=client.recv(BUFSIZ).decode("utf8")
    msg=bytes(f"{name} has joined the chat !","utf8")
    broadcast(msg,name) #broadcast welcome message

    while True:
        try:
            msg=client.recv(BUFSIZ)
            print(f"{name}: ",msg.decode("utf8"))
            if msg==bytes("{quit}","utf8"):
                broadcast(f"{name} has left the chat...","")
                client.send(bytes("{quit}","utf8"))
                client.close()
                persons.remove(person)
                break
            else:
                braoadcast(msg,name)
        except Exception as e:
            print("[EXCEPTION]",e)
            break


def wait_for_connection():


    """
    Wait for connection from new clients start new thread once connected
    :param SERVER : SOCKET
    :return :None
    """
    run = True
    while run:
        try:
            client,addr=SERVER.accept()
            person=Person(addr,name,client)
            persons.append(person)
            print(f"[CONNECTION] {addr} connected to server at {time.time()}")
            Thread(target=client_communication,args=(person,)).start()
        except Exception as e:
             print("[EXCEPTION]",e)
             run=False
    print("SERVER CRASHED")



if __name__=="__main__":
    SERVER.listen(MAX_CONNECTIONS)
    print("[STARTED]Waiting for connection.....")
    ACCEPT_THREAD = Thread(target=wait_for_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
