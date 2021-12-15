import json
import socket 
from _thread import start_new_thread

from models.Log import LogFile
from controllers.Requests import RequestHandler
from models import Responses
from models.Database import DataBase

class Connection:

  def __init__(self,log : LogFile, db : DataBase, addr : tuple) -> None:
    self.log = log
    self.DB = db
    self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
      self.socket.bind(addr)
    except Exception as e:
      self.log.write(f"Error While Binding\n {e}","error")
    self.AUTH_CONNECTIONS = []

  def run(self) -> None:
    self.socket.listen()
    print("Server Started")
    self.log.write("Server Started","success")
    while True:
      try:
        connection = self.socket.accept()
        print("Connection Accepted " + connection[1][0])
      except Exception as e:
        print("Error Occurred")
        self.log.write(f"Error Accepting/Listening \n {e}","error")
      
      start_new_thread(self.request_listener,(connection,))
  
  def broadcast(self, data : bytes) -> None:
    DISCONNECTED = []
    for connection in self.AUTH_CONNECTIONS:
      try:
        conn = connection[0]
        conn.sendall(data)
      except BrokenPipeError:
        DISCONNECTED.append(connection)
    for conn in DISCONNECTED:
      self.AUTH_CONNECTIONS.remove(conn)


  def request_listener(self, connection) -> None:
    while True:
      data = connection[0].recv(1024)
      if not data:
        break
      
      try:
        data = json.loads(data.decode("utf-8"))
        if type(data) != dict:
          raise ValueError
        RequestHandler(self, connection, data, self.log, self.DB)
      except Exception as e:
        data = Responses.BAD_REQUEST({"message" : "Insert Json Please."}).dump()
        connection[0].sendall(data)
        print(e)