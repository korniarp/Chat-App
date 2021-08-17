import threading
from socket import AF_INET,socket,SOCK_STREAM
from threading import Thread, Lock
import time

class Client:
    """
    for communication with server
    """
    HOST = "localhost"
    PORT = 6600
    ADDR = (HOST, PORT)
    BUFSIZ = 512

    def __init__(self,name):
        """
        Init object and send name to server
        :param name:str
        """
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        self.messages = []   #Keep track of messages
        receive_thread = Thread(target=self.receive_messages)
        receive_thread.start()
        self.send_message(name)
        self.lock = Lock()



    def receive_messages(self):
        """
        receive messages from server
        :return: None
        """
        while True:
            try:
                msg = self.client_socket.recv(self.BUFSIZ).decode()

                # make sure memory is safe to access
                self.lock.acquire()
                self.messages.append(msg)
                self.lock.release()
                # print(msg)
            except Exception as e:
                print("[EXPECTION4]", e)
                break

    def send_message(self,msg):

        """
        send message to server
        :param msg: str
        :return: None
        """
        self.client_socket.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            self.client_socket.close()

    def get_messages(self):
        """
        :returns a list of str messages
        :return:list[str]
        """
        messages_copy = self.messages[:]
        # make sure memory is safe to access
        self.lock.acquire()
        self.messages = []
        self.lock.release()
        return messages_copy

    def disconnect(self):
        self.send_message("{quit}")
