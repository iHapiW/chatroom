import json

class Base:
  code : int = 0
  type : str = ""
  content : dict = dict()
  def __init__(self, content : dict = None) -> None:
    if type(content) != dict and type(content) != type(None):
      raise ValueError("Content Should be Dict Type")
    if not content == None:
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

class OK(Base):
  code : int = 200
  type : str = "success"
  content : dict = {
    "message" : "OK."
  }

class CREATED(Base):
  code : int = 201
  type : str = "success"
  content : dict = {
    "message" : "Resource Created."
  }

class FOUND(Base):
  code : int = 202
  type : str = "success"
  content : dict = {
    "message" : "Resource Found."
  }

class BAD_REQUEST(Base):
  code : int = 400
  type : str = "error"
  content : dict = {
    "message" : "Bad Request!!"
  }

class UNAUTHORIZED(Base):
  code : int = 401
  type : str = "error"
  content : dict = {
    "message" : "Authentication Required."
  }

class NOT_FOUND(Base):
  code : int = 404
  type : str = "error"
  content : dict = {
    "message" : "Resource Not Found."
  }

class NOT_IMPLEMENTED(Base):
  code : int = 501
  type : str = "error"
  content : dict = {
    "message" : "Resource Not Created."
  }