#cpu usage


def getdata():
  import psutil
  a=psutil.cpu_percent(4)
  # Getting % usage of virtual_memory ( 3rd field)
  b=psutil.virtual_memory()[2]
  import subprocess as sp
  # raw strings avoid unicode encoding errors
  gpu_usage_cmd = r'(((Get-Counter "\GPU Engine(*engtype_3D)\Utilization Percentage").CounterSamples | where CookedValue).CookedValue | measure -sum).sum'

  def run_command(command):
      val = sp.run(['powershell', '-Command', command], capture_output=True).stdout.decode("ascii")

      return float(val.strip().replace(',', '.'))
  c= round(run_command(gpu_usage_cmd),2)
  return[a,c,b]

#print(getdata())


import socket
import pickle  # For serialization

# Client setup
HOST = "192.168.1.107"  # Server address
PORT = 12345       # Port to connect to

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
while True:
  # Data to send
  array = getdata()
  data = pickle.dumps(array)  # Serialize the array

  # Send data
  client_socket.sendall(data)
  print("Array sent to server")

  back = client_socket.recv(1024).decode('utf-8')
  print(f"Received from server: {back}")


  x1= input("Close connection enter y: ")
  if(x1=='y'):
    x2=['EXIT']
    data1 = pickle.dumps(x2)
    client_socket.sendall(data1)
    break

client_socket.close()