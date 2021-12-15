import json

class Base:
  type : str = ""
  content : dict = dict()
  def __init__(self, content : dict) -> None:
    if type(content) != dict:
      raise ValueError("Content Should be Dict Type")
    self.content = content
    
  def __dict__(self):
    result = dict()
    attribs = list(filter(lambda x : not x.startswith("_") ,dir(self)))
    attribs.remove("dump")

    for attrib in attribs:
      if type(getattr(self,attrib)) == type(dict):
        result[attrib] = dict()
        for item in getattr(self,attrib).items():
          attrib[item[0]] = item[1]
      else:
        result[attrib] = getattr(self,attrib)
    return result

  def dump(self):
    return json.dumps(self.__dict__()).encode("utf-8")

class Login(Base):
  type : str = "Login"
  content : dict = dict()

class Register(Base):
  type : str = "Register"
  content : dict = dict()

class Message(Base):
  type : str = "Message"
  content : dict = dict()

class DeleteAcc(Base):
  type : str = "DeleteAcc"
  content : dict = dict()