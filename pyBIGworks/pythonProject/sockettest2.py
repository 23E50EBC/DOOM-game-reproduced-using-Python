import socket

IP = "192.168.240.168"

PORT = 50000

buffen = 512

sk2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

sk2.connect((IP,PORT))

toSend = "1111"

while True:
    # toSend = input(">>")
    # if toSend =='0000':
    #     break

    sk2.send(toSend.encode())

    recved = sk2.recv(buffen)

    if not recved :
        break

    print(recved.decode())

sk2.close()