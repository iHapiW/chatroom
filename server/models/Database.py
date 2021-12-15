import asyncio
import asyncpg
import string
import random

from models.Log import LogFile

class DataBase():
  characters = list(string.ascii_letters + string.digits + "!@#$%^&*")
  DB = None

  def __init__(self,db_user : str, db_passwd : str, db_name : str, log : LogFile) -> None:
    self.log = log
    try:
      self.event_loop = asyncio.get_event_loop()
      self.DB = self.event_loop.run_until_complete(asyncpg.create_pool(dsn = f"postgres://{db_user}:{db_passwd}@localhost:5432/{db_name}"))
      self.event_loop.run_until_complete(self.DB.execute('CREATE TABLE IF NOT EXISTS test_db (username TEXT, passcode TEXT, token TEXT)'))
      self.log.write("Logged In to DataBase", "success")
    except asyncpg.exceptions.InvalidPasswordError as e:
      self.log.write(f"Database Credential Error \n{e}", "error")

  def generate_random_token(self):
    length = 64
    random.shuffle(self.characters)
    password = []
    for i in range(length):
      password.append(random.choice(self.characters))
    random.shuffle(password)
    return("".join(password))

  def get_token(self):
    dup = True
    while(dup):
      token = self.generate_random_token()
      all_token_data = self.event_loop.run_until_complete(self.DB.fetch('SELECT token FROM test_db'))
      all_tokens = []
      for b in all_token_data:
        tkn = b.get("token")
        all_tokens.append(tkn)
      if token in all_tokens:
        self.log.write("Duplicated Token Generated","warning")
      else:
        dup = False
        return token

  def register(self, username, passwd,ip):
    all_usernames_data = self.event_loop.run_until_complete(self.DB.fetch('SELECT username FROM test_db'))
    all_usernames = []
    for a in all_usernames_data:
      ur = a.get("username")
      all_usernames.append(ur)
    if username in all_usernames:
      self.log.write("Duplicate User Entered")
      return False

    gn_token = self.get_token()

    self.event_loop.run_until_complete(self.DB.execute('INSERT INTO test_db(username, passcode, token) VALUES ($1, $2, $3)', username, passwd, gn_token))
    self.log.write(f"Added User To Database! [\t{username} | {passwd} | {gn_token}\t]","success")
    self.log.write(f"{ip} Registered {username}")
    return gn_token

  def login(self, username, passwd, ip):
    try:
      token = self.event_loop.run_until_complete(self.DB.fetch('SELECT token FROM test_db WHERE username = $1 AND passcode = $2', username, passwd))
      token = token[0].get("token")
      self.log.write(f"{ip} : Connected Using {passwd}")
      return str(token)
    except:
      self.log.write(f"{ip} : Could'nt Login Using {passwd}")
      return False
      
  def validateToken(self, token):
    try:
      username = self.event_loop.run_until_complete(self.DB.fetch('SELECT username FROM test_db WHERE token = $1', token))
      username = username[0].get("username")
      return str(username)
    except:
      self.log.write("Invalid Token","error")
      return False

  def delete_acc(self, token):
    try:
      username = self.event_loop.run_until_complete(self.validateToken(token))
      if not username:
        self.log.write("User Not Found to Delete Account")
        return False
      stat = self.event_loop.run_until_complete(self.DB.execute("DELETE FROM test_db WHERE token = $1", token))
      if stat == "DELETE 1":
        self.log.write(f"{username} Deleted Account")
        return True
      if stat == "DELETE 0":
        self.log.write("Not Deleted", "warning")
        return False
    except:
      self.log.write("Error Occured While Deleteing Account", "error")
      return False