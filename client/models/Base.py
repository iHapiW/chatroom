from functools import partial

from PyQt5 import QtGui
from PyQt5.QtWidgets import QLabel, QMainWindow

from models.User import User
from views.Base import Ui_MainWindow
from controllers.Signals import send_button_slot

class MainWindow(Ui_MainWindow, QMainWindow):
  def __init__(self):
    super().__init__()
    self.setupUi(self)
    self.setFixedSize(362,431)
    self.retranslateUi(self)
    self.user = User("")

  def connectSignals(self):
    chatSlot = partial(send_button_slot,self.chatLayout,self.inputText,self.user)
    self.sendButton.clicked.connect(chatSlot)
    self.inputText.returnPressed.connect(chatSlot)
  
  def configStatusBar(self):
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
    address.setText("IP: 127.0.0.1:5050")
    address.setStyleSheet("color: #206E4A;")
    self.statusbar.addWidget(address)

