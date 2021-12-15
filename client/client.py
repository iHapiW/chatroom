import sys
sys.dont_write_bytecode = True
import json

from PyQt5.QtWidgets import QApplication
from models.Authenticate import Dialog
from models.Base import MainWindow

if __name__ == "__main__":

  try:
    cfg_file = open("config.json","r")
    config = json.loads(cfg_file.read())
    ip = config['server_ip']
    port = config['server_port']

  except (IndexError, FileNotFoundError, json.decoder.JSONDecodeError):
    cfg_file = open("config.json","w")
    demo = {"server_ip" : "127.0.0.1", "server_port" : 65432}
    cfg_file.write(json.dumps(demo))
    ip = demo['server_ip']
    port = demo['server_port']

  app = QApplication(sys.argv)
  app.aboutToQuit.connect(lambda : sys.exit())
  main = MainWindow()
  dial = Dialog(main,(ip,port))
  dial.exec()

  sys.exit(app.exec())