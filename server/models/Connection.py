from json import loads, dumps
from socket import AF_INET, SOCK_STREAM, socket
from _thread import start_new_thread

from controllers.Requests import request_handler

class Connection:

  def __init__(self) -> None:
    self.socket = socket(AF_INET,SOCK_STREAM)
    self.socket.bind(("0.0.0.0",65432))
    self.CONNECTIONS = []

  def run(self) -> None:
    while True:
      self.socket.listen()
      connection = self.socket.accept()
      self.CONNECTIONS.append(connection)
      start_new_thread(self.request_listener,(connection,))
  
  def broadcast(self, data : dict) -> None:
    try:
      for connection in self.CONNECTIONS:
        conn = connection[0]
        conn.send(dumps(data).encode("utf-8"))
    except :
      pass

  def request_listener(self, connection) -> None:
    full_data = b""

    while True:
      data = connection[0].recv(1024)
      if not data:
        break
      full_data += data
    
    try:
      full_data = loads(full_data.decode("utf-8"))
    except:
      connection[0].sendall()
    
    request_handler(connection,full_data)