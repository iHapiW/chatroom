import sys
sys.dont_write_bytecode = True

from PyQt5.QtWidgets import QApplication

from models.Base import MainWindow

if __name__ == "__main__":
  app = QApplication(sys.argv)
  win = MainWindow()
  win.show()
  sys.exit(app.exec())