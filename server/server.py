from json import decoder
import sys
import json
sys.dont_write_bytecode = True

import atexit

from models.Connection import Connection
from models.Log import LogFile
from models.Database import DataBase
from controllers.utils import do_at_exit

def main():
  try:
    cfg_file = open("config.json","r")
    config = json.loads(cfg_file.read())
    ip = config['server_ip']
    port = config['server_port']
    log_dir_name = config['log_directory_name']
    log_file_name = config['log_file_name']
    db_user = config['db_user']
    db_passwd = config['db_user_passwd']
    db_name = config['db_name']
  except FileNotFoundError:
    cfg_file = open("config.json","w")
    demo = {"server_ip" : "0.0.0.0", "server_port" : 65432, "log_directory_name" : "Logs", "log_file_name" : "log.txt", "db_user" : "", "db_user_passwd" : "", "db_name" : ""}
    cfg_file.write(json.dumps(demo))
    print("Config in config.json")
    input("")
    sys.exit()
  except (KeyError, json.decoder.JSONDecodeError):
    print("Malformed Config!\n you can delete config.json, again run app to make standard config.json for you :)")
    input("")
    sys.exit()

  log = LogFile(log_file_name, log_dir_name)
  atexit.register(do_at_exit,log)

  db = DataBase(db_user, db_passwd, db_name, log)

  try:
    server = Connection(log, db, (ip,port))
    server.run()
  except KeyboardInterrupt:
    log.write("Server Closed","warning")

if __name__ == "__main__":
  main()