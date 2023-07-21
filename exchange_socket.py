import socket
import pickle



class MyClass:
    def __init__(self, value):
        self.value = value

def start_client():
    # create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # get local machine name
    host = socket.gethostname()

    port = 9999

    # connection to hostname on the port.
    client_socket.connect((host, port))

    # create an object
    my_obj = MyClass("Hello")

    # serialize the object
    my_obj_bytes = pickle.dumps(my_obj)

    # send the serialized object to the server
    client_socket.send(my_obj_bytes)

    # close the connection
    client_socket.close()

start_client()

