import datetime
from os import path, mkdir

class LogFile:
  def __init__(self,filename : str, filedir : str) -> None:
    try:
      self.log = open(path.join(filedir,filename),"w")
    except FileNotFoundError:
      mkdir(filedir)
      self.log = open(path.join(filedir,filename),"w")

  def write(self, message : str, type : str = None):
    prefix = None
    if message == None:
      raise ValueError

    if type == None:
      prefix = "[*]"
    elif type == "success":
      prefix = "[+]"
    elif type == "warning":
      prefix = "[!]"
    elif type == "error":
      prefix = "[-]"
    else:
      raise ValueError
    
    time = datetime.datetime.now()
    year = time.year
    month = time.month
    day = time.day
    hour = time.hour
    minute = time.minute
    second = time.second

    self.log.write(f"[{year}-{month}-{day}] | [{hour}:{minute}:{second}] {prefix} {message}\n")

  def close(self):
    self.log.close()