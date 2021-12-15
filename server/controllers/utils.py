import re

from models.Log import LogFile

def format_input(text : str) -> str:
  text = text.strip()
  word_array = text.split()
  formatted_words = []
  for word in word_array:
    if len(word) > 20:
      x = 0
      temp_list = []
      while x < len(word):
        if x+20 < len(word):
          temp_list.append(word[x:x+20])
        else:
          temp_list.append(word[x:])
        x+=20
      for temp_word in temp_list:
        formatted_words.append(temp_word)
    else:
      formatted_words.append(word)
  text = " ".join(formatted_words)
  return text

def valid_username(username : str) -> bool:
  username = username.strip()
  if len(username) > 20 or len(username) < 3:
    return False
  pattern = re.compile("^[a-zA-Z0-9._]+$")
  matched = bool(re.match(pattern,username))
  return matched

def do_at_exit(log : LogFile):
  print("\nServer Closed")
  log.close()