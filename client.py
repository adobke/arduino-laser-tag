import socket

def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    sock.send(message)
    response = sock.recv(1024)
    #print "Received: %s" % response
    sock.close()
    return response

ip = '127.0.0.1'

def main(port = 4242):
    while True:
        cin = raw_input(">>< ")
        print client(ip, port, cin)



if __name__ == "__main__":
    main()
