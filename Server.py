from tkinter import *
from tkinter.ttk import *
from socket import *
from select import *

import sys

HOST = "localhost"
PORT = 33110

server = socket(AF_INET, SOCK_STREAM)

server.bind((HOST, PORT))

server.listen(5)

clients = []
id_client = {}


def getClient():
     use = []
     for client in clients:
          use.append(client[0])
     #print(use)
     return use

while 1:
     #try:
          read, write, error = select([server], [], [], 0)
          if(len(read)):
               client, address = server.accept()
               clients.append([client, address, []])
               #print(client)
               id_client[len(id_client)+1] = clients[-1][0]
               #for i in range(len(id_client)):
               #data = str(id_client.keys())
               #data = []
               data = []
               for a in id_client.keys():
                    data.append(a)
               #print(data)
               for i in data:
                    try:
                         b = id_client[i].send(str.encode(str(data)))
                    except:
                         for y in clients:
                              if y[0] == id_client[i]:
                                   y[0].close()
                                   print("a")
                                   clients.remove(y)
                         id_client.pop(i)
                                   #id_client.pop(i)
                              #print("Tipe clients:",type(y[0]))
                              #print("Tipe id_client:",type(id_client[i]))
                    #print(id_client[data[0]])
               #print(clients)
               #print(id_client)
               #print(id_client[1])
               #print(id_client)
               #print(address[1])
               
          use = getClient()
          try:
               read, write, error = select(use, [], [], 0)
               if(len(read)):
                    for client in read:
                         #print(client)
                         data = client.recv(1024)
                         #print(bytes.decode(data)[2:])
                         tujuan = int(bytes.decode(data)[0])
                         #print(id_client[tujuan])
                         if(data == 0):
                              for c in clients:
                                   if c[0] == client:
                                        clients.remove(c)
                                        break
                         else:
                              for c in clients:
                                   c[2].append(data)
                         
          except:
               pass
          try:
               use = getClient()
               read, write, error = select([], use, [], 0)
               if(len(write)):
                    for client in write:
                         for c in clients:
                              if c[0] == client:
                                   for data in c[2]:
                                        #print(client)
                                        #value = str.encode(str(data[2:]))
                                        sent = id_client[tujuan].send(data)
                                        c[2].remove(data)
                                   break
                         break
          except:
               pass
               
    # except:
     #     pass
                    
