import json

def request_handler(connection,data):
  print(f"({connection[1][0]}) Sent : {json.dumps(data)}")