from functools import partial
import sys

from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit
from PyQt5.QtCore import Qt

from models.User import User
from views.Authenticate import Ui_Dialog
from controllers.Signals import login, register
from models.Connection import Connection
from models.Base import MainWindow

class Dialog(Ui_Dialog,QDialog):
  def __init__(self,base : MainWindow ,addr : tuple) -> None:
    super().__init__()
    self.setupUi(self)
    self.retranslateUi(self)
    self.passwdInput.setEchoMode(QLineEdit.Password)
    self.show()
    self.addr = addr
    self.base = base
    self.connection = self.createConnection(addr)
    self.connectSignals()
    
  def connectSignals(self) -> None:
    if self.connection != None:
      self.reg.clicked.connect(partial(register,self))
      self.login.clicked.connect(partial(login,self))
      self.passwdInput.returnPressed.connect(partial(login,self))
      self.usernameInput.returnPressed.connect(partial(login,self))
    self.rejected.connect(lambda : sys.exit())

  def createConnection(self,addr) -> Connection:
    try:
      connection = Connection(addr)
      return connection
    except :
      self.showError("Connection Timed Out\nRestart The App (Server may Down)")
      

  def showError(self,message):
      self.clearError()
      label = QLabel()
      label.setText("**Error**")
      label.setStyleSheet("color : red; font-size: 25px")
      label.setWordWrap(False)
      label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
      label.setTextFormat(Qt.MarkdownText)
      content = QLabel()
      content.setText(message)
      content.setStyleSheet("color : red; font-size: 15px")
      content.setWordWrap(True)
      content.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
      content.setTextFormat(Qt.AutoText)
      self.errorLayout.addWidget(label)
      self.errorLayout.addWidget(content)
    
  def clearError(self):
      for i in reversed(range(self.errorLayout.count())): 
        self.errorLayout.itemAt(i).widget().setParent(None)
  
  def authenticated(self, user : User,):
    self.base.configWindow(user, self.connection)