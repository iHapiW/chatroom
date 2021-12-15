from PyQt5.QtWidgets import QMainWindow

def get_messages(base : QMainWindow):
  base.connection.socket.settimeout(None)
  while True:
    data = base.connection.recieve()
    try:
      base.new_message.emit(data['content']['text'],base)
    except KeyError:
      print("keyError")