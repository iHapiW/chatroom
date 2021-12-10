from PyQt5 import QtGui
from PyQt5.QtWidgets import QLabel, QMainWindow

from views.Base import Ui_MainWindow
from controllers.Signals import send_button_slot

class MainWindow(Ui_MainWindow, QMainWindow):
  def __init__(self):
    super().__init__()
    self.setupUi(self)
    self.setFixedSize(362,431)
    self.retranslateUi(self)
    self.connectSignals()
    self.configStatusBar()

  def connectSignals(self):
    self.sendButton.clicked.connect(send_button_slot)
  
  def configStatusBar(self):
    user = QLabel()
    font = QtGui.QFont()
    font.setFamily("Cantarell")
    font.setPointSize(9)
    user.setFont(font)
    user.setText("Username : iHapiW")
    user.setStyleSheet("color: #206E4A;")
    self.statusbar.addPermanentWidget(user)
    address = QLabel()
    address.setFont(font)
    address.setText("IP: 127.0.0.1:5050")
    address.setStyleSheet("color: #206E4A;")
    self.statusbar.addWidget(address)

