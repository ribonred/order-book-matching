import socket
import pickle

def start_server():
    # create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # get local machine name
    host = socket.gethostname()

    port = 9999

    # bind to the port
    server_socket.bind((host, port))

    # queue up to 5 requests
    server_socket.listen(5)

    while True:
        # establish a connection
        client_socket, addr = server_socket.accept()

        print("Got a connection from %s" % str(addr))

        data = client_socket.recv(1024)
        obj = pickle.loads(data)
        print("Received object: ", obj)

        # close the connection
        client_socket.close()

start_server()
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
