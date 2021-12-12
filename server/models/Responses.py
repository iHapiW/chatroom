class Base:
  code : int = 0
  type : str = ""
  message : str = ""
  def __init__(self, message : str) -> None:
    if not message == None:
      self.message = message

class OK(Base):
  code : int = 200
  type : str = "success"
  message : str = "Operation Done Successfully."
  def __init__(self, message : str) -> None:
    super().__init__(message)

class CREATED(Base):
  code : int = 201
  type : str = "success"
  message : str = "Created Resurce."
  def __init__(self, message : str) -> None:
    super().__init__(message)

class FOUND(Base):
  code : int = 202
  type : str = "success"
  message : str = "Data Malformed!"
  def __init__(self, message : str) -> None:
    super().__init__(message)

class BAD_REQUEST(Base):
  code : int = 400
  type : str = "error"
  message : str = "Data Malformed!"
  def __init__(self, message : str) -> None:
    super().__init__(message)

class UNAUTHORIZED(Base):
  code : int = 401
  type : str = "error"
  message : str = "Youre unAuthorized"
  def __init__(self, message : str) -> None:
    super().__init__(message)
