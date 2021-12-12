from models.Connection import Connection
from controllers.utils import response

if __name__ == "__main__":
  server = Connection()
  server.run()