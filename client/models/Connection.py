from socket import AF_INET, SOCK_STREAM, socket, timeout
from json import loads

class Connection:

  def __init__(self, addr : tuple) -> None:
    self.socket = socket(AF_INET,SOCK_STREAM)
    self.socket.settimeout(5)
    self.addr = addr
    try:
      self.socket.connect(self.addr)
    except timeout:
      self.socket.close()
      raise timeout("Timout Error")

  def send(self, data : bytes) -> None:
    self.socket.sendall(data)
  
  def recieve(self) -> bytes:
    data = self.socket.recv(1024)
    response = loads(data.decode('utf-8'))
    return response