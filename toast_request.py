import requests

url="http://78c0bdc4.ngrok.io/sendsms"

def sendsms_task():
  print("INSIDE REQUEST")
  response = requests.post(url)
  print(str(response.status_code))

