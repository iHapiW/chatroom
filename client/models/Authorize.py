from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QMainWindow
from PyQt5.QtGui import QKeyEvent

from views.Authorize import Ui_Dialog
from controllers.Signals import authorization_accepted, authorization_rejected

class Dialog(Ui_Dialog,QDialog):
  def __init__(self,base : QMainWindow) -> None:
    super().__init__()
    self.setupUi(self)
    self.retranslateUi(self)
    self.connectSignals()
    self.base = base
  def connectSignals(self) -> None:
    self.ok.clicked.connect(partial(authorization_accepted,self.usernameInput,self.errorLayout,self))
    self.cancel.clicked.connect(authorization_rejected)

  def keyPressEvent(self, a0: QKeyEvent) -> None:
    if a0.key() == Qt.Key_Enter or a0.key() == Qt.Key_Return:
      return self.ok.click()
    if a0.key() == Qt.Key_Escape:
      return self.cancel.click()
    return super().keyPressEvent(a0)

  def setText(self,user):
    self.base.user = user
    self.base.configStatusBar()
    self.base.connectSignals()