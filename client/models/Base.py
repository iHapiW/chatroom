from _thread import start_new_thread
from functools import partial

from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel, QMainWindow

from models.User import User
from views.Base import Ui_MainWindow
from models.Connection import Connection
from controllers.Signals import send_message, print_message
from controllers.utils import get_messages

class MainWindow(Ui_MainWindow, QMainWindow):

  new_message = pyqtSignal(str,QMainWindow)

  def __init__(self):
    super().__init__()
    self.setupUi(self)
    self.setFixedSize(362,431)
    self.retranslateUi(self)

  def configWindow(self, user : User, connection : Connection):
    self.user = user
    self.connection = connection
    self.configStatusBar()
    self.connectSignals()
    self.show()
    start_new_thread(get_messages,(self,))

  def connectSignals(self):
    self.inputText.returnPressed.connect(partial(send_message,self))
    self.sendButton.clicked.connect(partial(send_message,self))
    self.new_message.connect(print_message)

  def configStatusBar(self):
    self.addr = self.connection.addr
    username = QLabel()
    font = QtGui.QFont()
    font.setFamily("Cantarell")
    font.setPointSize(9)
    username.setFont(font)
    username.setText(f"Username : {self.user.username}")
    username.setStyleSheet("color: #206E4A;")
    self.statusbar.addPermanentWidget(username)

    address = QLabel()
    address.setFont(font)
    address.setText(f"IP: {self.addr[0]}:{self.addr[1]}")
    address.setStyleSheet("color: #206E4A;")
    self.statusbar.addWidget(address)

  def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
    super().closeEvent(a0)