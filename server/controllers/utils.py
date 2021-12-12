from json import loads, dumps

from models.Responses import Base, OK, CREATED, FOUND, BAD_REQUEST, UNAUTHORIZED

def response(resp_name : str, message : str = None) -> bytes:
  resp_name = resp_name.lower()
  if resp_name == "ok":
    data = OK(message)
  elif resp_name == "created":
    data = CREATED(message)
  elif resp_name == "found":
    data = FOUND(message)
  elif resp_name == "bad_request":
    data = BAD_REQUEST(message)
  elif resp_name == "unauthorized":
    data = UNAUTHORIZED(message)
  else :
    raise ValueError("Invalid Response Name")

  attributes = list(filter(lambda x : not x.startswith("_"),dir(Base)))
  dictionary = dict()
  for attribute in attributes:
    attr_data = getattr(data,attribute)
    dictionary[attribute] = attr_data
  
  return dumps(dictionary).encode("utf-8")