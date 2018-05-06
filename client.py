import socket

host: str = '192.168.4.1'
port: int = 6677


def new_sock(host: str, port: int) -> socket:
    """
    Creates new tcp connection with specified host and port
    :param host:
    :param port:
    :return:
    """
    s = socket.socket()
    s.settimeout(.5)
    s.connect((host, port))
    return s


def send_number(i):
    """
    Sends a number to the server
    :param i:
    """
    s = new_sock(host, port)
    s.send('{}'.format(i).encode())
    s.close()


def get_number(i):
    """
    Gets number from server and splits the values
    :param i:
    :return:
    """
    s = new_sock(host, port)
    s.send('{}'.format(i).encode())
    number = s.recv(1024)
    s.close()
    print(number)
    return [number.split()[0], number.split()[1]]
