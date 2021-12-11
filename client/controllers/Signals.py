import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QVBoxLayout, QTextEdit, QFrame

from models.User import User
from controllers.utils import format_input, valid_username

def send_button_slot(layout : QVBoxLayout ,inputText : QLineEdit, user : User) -> None:
  text = format_input(inputText.displayText())
  if len(text) > 0:
    inputText.setText("")
    label = QLabel()
    label.setText(user.username + " > " + text)
    label.setWordWrap(True)
    layout.addWidget(label)
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    layout.addWidget(line)
    

def authorization_accepted(username_input : QLineEdit, error_layout : QVBoxLayout, dialog : QDialog) -> None:
  username = username_input.displayText()
  dialog.setMinimumHeight(111)
  dialog.setMaximumHeight(111)
  for i in reversed(range(error_layout.count())):
    error_layout.itemAt(i).widget().setParent(None)
  if not valid_username(username):
    dialog.setMinimumHeight(200)
    dialog.setMaximumHeight(200)
    error = QLabel()
    error.setText("Error: Username Should Only Contain [A-Z][a-z][0-9] or underline & Between 8 to 20 Characters!")
    error.setStyleSheet("color:red")
    error.setWordWrap(True)
    error.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
    error_layout.addWidget(error)
  else:
    dialog.setText(User(username))
    dialog.accept()
    
def authorization_rejected() -> None:
  sys.exit()