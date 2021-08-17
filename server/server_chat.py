import socket
from threading import Thread
import time
from person import Person

# print_lock = threading.Lock()

# GLOBAL CONSTANTS
HOST = ""
PORT = 6600
MAX_CONNECTIONS = 10
BUFSIZ = 1024

# GLOBAL VARIABLES
persons = []
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))   # set up server


def broadcast(msg,name):
    """
    send new messages to all clients
    :param msg: bytes["utf8"]
    :param name: str
    :return:
    """
    for person in persons:
        client = person.client
        client.send(bytes(name,"utf8")+msg)


def client_communication(person):
    """
      Thread to handle all messages from client
      :param person : Person
      :return :None
      """


    client = person.client
    # addr = person.addr

    # first message received is always the person's name
    name = client.recv(BUFSIZ).decode("utf8")
    person.set_name(name)
    msg = bytes(f"{name} has joined the chat !", "utf8")
    broadcast(msg,"")  # broadcast welcome message

    while True: # wait for any messages from person
        try:
            msg=client.recv(BUFSIZ)                       # wait for receival from client
            if msg == bytes("{quit}","utf8"):             # if message is quit , then disconnect client
                # client.send(bytes("{quit}","utf8"))
                client.close()
                persons.remove(person)
                broadcast(bytes(f"{name} has left the chat...","utf8"), "")

                print(f"[DISCONNECTED] {name} disconnected.")
                break
            else:                                       # otherwise send message to all other clients
                broadcast(msg,name+": ")
                print(f"{name}: ", msg.decode("utf8"))
        except Exception as e:
            print("[EXCEPTION2]",e)
            break




def Main():

    print("Server is binded to %s"%(PORT))
    s.listen(MAX_CONNECTIONS)           # open server to listen for connections
    print("[STARTED]Waiting for connection.....")

    while True:
        try:
            client,addr = s.accept()        # wait for any new connections
            # print_lock.acquire()
            person = Person(addr, client)       # create new person for connection
            persons.append(person)
            print("Connected to : ",addr[0],":",addr[1],f"at {time.asctime()}")
            # start_new_thread(client_communication,(client,addr))
            Thread(target=client_communication,args=(person,)).start()
        except Exception as e:
            print("[EXCEPTION1]", e)
            break
    print("SERVER CRASHED")
    s.close()




if __name__ == "__main__":
    Main()