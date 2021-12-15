from PyQt5.QtWidgets import QDialog, QLineEdit, QMainWindow, QFrame, QLabel
from models.User import User

from models.Requests import Login, Message, Register

def register(dialog : QDialog) -> None:
  dialog.clearError()
  usernameInput : QLineEdit = dialog.usernameInput
  passwdInput : QLineEdit = dialog.passwdInput
  username = usernameInput.text()
  password = passwdInput.text()
  request = Register({"uname" : username, "passwd" : password})
  dialog.connection.send(request.dump())
  response = dialog.connection.recieve()
  if response['type'] == "error":
    dialog.showError(response['content']['message'])
  elif response['code'] == 201:
    dialog.authenticated(User(username,password,response['content']['token']))
    dialog.accept()

def login(dialog : QDialog):
  dialog.clearError()
  usernameInput : QLineEdit = dialog.usernameInput
  passwdInput : QLineEdit = dialog.passwdInput
  username = usernameInput.text()
  password = passwdInput.text()
  request = Login({"uname" : username, "passwd": password})
  dialog.connection.send(request.dump())
  response = dialog.connection.recieve()
  if response['type'] == "error":
    dialog.showError(response['content']['message'])
  elif response['code'] == 202:
    dialog.authenticated(User(username,password,response['content']['token']))
    dialog.accept()

def send_message(base : QMainWindow):
  input_text : QLineEdit = base.inputText
  text = input_text.text()
  token = base.user.token
  request = Message({"text" : text, "token" : token})
  base.connection.send(request.dump())
  input_text.setText("")

def print_message(text : str, base : QMainWindow):
  message = QLabel()
  message.setText(text)
  message.setWordWrap(True)
  base.chatLayout.addWidget(message)
  line = QFrame()
  line.setFrameShape(QFrame.HLine)
  base.chatLayout.addWidget(line)