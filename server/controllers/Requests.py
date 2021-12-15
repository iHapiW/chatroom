from controllers.utils import format_input, valid_username
from models import Responses
from models.Database import DataBase
from models.Log import LogFile

class RequestHandler:
  def __init__(self, server, connection : tuple, data : dict, log : LogFile, db : DataBase) -> None:
    self.sck = connection[0]
    self.addr = connection[1]
    self.log = log
    self.DB = db
    self.server = server

    try:
      if data['type'].lower() == "register":
        self.register(data)
      if data['type'].lower() == "login":
        self.login(data)
      if data['type'].lower() == "message":
        self.message(data)
    except KeyError:
      self.sck.sendall(Responses.BAD_REQUEST().dump())
  

  def register(self,data : dict) -> None:
    try:
      content = data['content']
      if valid_username(content['uname']):
        if len(content['passwd']) < 5:
          self.sck.sendall(Responses.BAD_REQUEST({"message" : "Password Should Contain At least 5 Characters"}).dump())
        else:
          result = self.DB.register(content['uname'],content['passwd'],self.addr[0])
          if not result:
            self.sck.sendall(Responses.NOT_IMPLEMENTED({"message":"Username Already Exist"}).dump())
          else :
            self.sck.sendall(Responses.CREATED({"message" : "User Registered","token" : result}).dump())
      else:
        self.sck.sendall(Responses.NOT_IMPLEMENTED({"message":"Username Should Only Consist of [A-Z][a-z][0-9][._] With 3 to 20 Characters"}).dump())
    except KeyError:
      self.sck.sendall(Responses.BAD_REQUEST({"content":"Input Malformed!"}).dump())
  
  
  def login(self,data : dict) -> None:
    try:
      content = data['content']
      if valid_username(content['uname']):
        if len(content['passwd']) < 5:
          self.sck.sendall(Responses.BAD_REQUEST({"message" : "Password Should Contain At least 5 Characters"}).dump())
        else:
          result = self.DB.login(content['uname'],content['passwd'],self.addr[0])
          if not result:
            self.sck.sendall(Responses.NOT_FOUND({"message": "Invalid Username Or Password"}).dump())
          else:
            self.sck.sendall(Responses.FOUND({"message": "Logged in", "token" : result}).dump())
            self.server.AUTH_CONNECTIONS.append((self.sck,self.addr))
      else:
        self.sck.sendall(Responses.NOT_FOUND({"message":"Username Should Only Consist of [A-Z][a-z][0-9][._] With 3 to 20 Characters"}).dump())
    except KeyError:
      self.sck.sendall(Responses.BAD_REQUEST({"content": "Input Malformed!"}).dump())
  
  def message(self,data : dict):
    try:
      content = data['content']
      if len(content['text']) == 0:
        return
      formatted_text = format_input(content['text'])
      token = content['token']
      username = self.DB.validateToken(token)
      if not username:
        self.sck.sendall(Responses.BAD_REQUEST({"content": "Invalid Token"}).dump())
      else:
        formatted_text = f"{username} > {formatted_text}"
        self.server.broadcast(Responses.OK({"text" : formatted_text}).dump())
    except KeyError:
      self.sck.sendall(Responses.BAD_REQUEST({"content": "Input Malformed!"}).dump())