import sys
sys.dont_write_bytecode = True

from PyQt5.QtWidgets import QApplication

from models.Base import MainWindow
from models.Authorize import Dialog

if __name__ == "__main__":
  app = QApplication(sys.argv)
  base = MainWindow()
  dial = Dialog(base)
  dial.exec()
  base.show()
  sys.exit(app.exec_())