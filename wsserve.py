import time
import socket
import sys
import threading
import struct
import hashlib

MYIP = '127.0.0.1'
PORT = 8001

clients = []
def start(hfunc= lambda x: x):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # listen for upto 50 cnxns on port 8000
    sock.bind((MYIP, PORT))
    sock.listen(50)
    
    while True:
        csock,caddr = sock.accept()
        clients.append(csock)
        print "Connection from: ", caddr
        # Start a thread to service each cnxn
        t = threading.Thread(target=handle_cnxn, args=(csock,caddr,hfunc))
        t.start()

def sendToAll(data):
    def send(data,csock):
        first_byte = chr(0x00)
        payload = data.encode('utf-8')
        pl = first_byte + payload + chr(0xFF)
        csock.send(pl)
   
    for client in clients:
        send(data,client)


def handle_cnxn(csock,addr,hfunc):
    shake1 = csock.recv(1024)
    shakelist = shake1.split("\r\n")
    # The body follows a \r\n after the 'headers'
    body = shake1.split("\r\n\r\n")[1]
    client = shakelist[4][8:]
    
    # Extract key1 and key2 
    for elem in shakelist:
        if elem.startswith("Sec-WebSocket-Key1:"):
            key1 = elem[20:]  # Sec-WebSocket-Key1: is 20 chars
        elif elem.startswith("Sec-WebSocket-Key2:"):
            key2 = elem[20:]
        else:
            continue

    # Count spaces
    nums1 = key1.count(" ")
    nums2 = key2.count(" ")
    # Join digits in the key
    num1 = ''.join([x for x in key1 if x.isdigit()])
    num2 = ''.join([x for x in key2 if x.isdigit()])
    
    # Divide the digits by the num of spaces
    key1 = int(int(num1)/int(nums1))
    key2 = int(int(num2)/int(nums2))

    # Pack into Network byte ordered 32 bit ints
    key1 = struct.pack("!I", key1)
    key2 = struct.pack("!I", key2)

    # Concat key1, key2, and the the body of the client handshake and take the md5 sum of it
    key = key1 + key2 + body
    m = hashlib.md5()
    m.update(key)
    d = m.digest()
    
    # Send 'headers'
    csock.send("HTTP/1.1 101 WebSocket Protocol Handshake\r\n")
    csock.send("Upgrade: WebSocket\r\n")
    csock.send("Connection: Upgrade\r\n")
    csock.send("Sec-WebSocket-Origin: " + client + "\r\n")
    csock.send("Sec-WebSocket-Location: ws://" + MYIP +":" + str(PORT)+"/\r\n")
    csock.send("Sec-WebSocket-Protocol: ltag\r\n")
    csock.send("\r\n")
    #Send digest
    csock.send(d)

    # Message framing - 0x00 utf-8-encoded-body 0xFF
    def send(data):
        first_byte = chr(0x00)
        payload = data.encode('utf-8')
        pl = first_byte + payload + chr(0xFF)
        #print "SENDD " + pl
        csock.send(pl)

    # This is dependent on you - what you wish to send to the browser
    i = 0
    send(u"%s" % "hi")
    while True:
        data = csock.recv(1024)
        if data == '':
            print str(addr) + " left"
            clients.remove(csock)
            break
        else:
            send(hfunc(data[1:-1]))




if __name__ == "__main__":
    start()
