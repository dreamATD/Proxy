from socket import *
import sys


tcpSerSock = socket(AF_INET, SOCK_STREAM)
# Fill in start.
tcpSerSock.bind(('', 6555))
tcpSerSock.listen(5)
# Fill in end.
while True:
    # Start receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from: ', addr)
    message = tcpCliSock.recv(4096).decode()

    # Extract the filename from the given message
    print(message.split()[1])
    filename = message.split()[1].partition("/")[2]
    fileExist = 'false'
    filetouse = '/' + filename
    try:
        # Check wether the file exist in the cache
        f = open(filetouse[1:], "r")
        outputdata = f.readlines()
        fileExist = 'true'
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send('HTTP/1.0 200 OK\r\n\r\n'.encode())
        # Fill in start.
        for s in outputdata:
            tcpCliSock.send(s.encode())
        # Fill in end.

        print('Read from cache')
        # Error handling for file not found in cache
    except IOError:
        if fileExist == 'false':
            # Create a socket on the proxyserver
            c = socket(AF_INET, SOCK_STREAM)
            hostn = filename.replace('www.', '', 1)
            print('Host Name: ', hostn)
            try:
                # Connect to the socket to port 80
                # Fill in start.
                c.connect((hostn, 80))
                # Fill in end.
                # Create a temporary file on this socket and ask port 80 for the file requested by the client

                c.send(("GET " + "http://" + filename + " HTTP/1.0\r\n\r\n").encode())

                msg = ''
                while True:
                    bufs2c = c.recv(1024)
                    if not bufs2c:
                        break
                    print(bufs2c.decode())
                    msg += bufs2c.decode()

                print(msg)
                tcpCliSock.sendall(msg.encode())
            except:
                print('Illegal request')
        else:
            # HTTP response message for file not found
            # Fill in start.
            print('File Not Found')
            a = 2
            # Fill in end.
            # Close the client and the server sockets
    tcpCliSock.close()

# Fill in start.
tcpSerSock.close()
# Fill in end.