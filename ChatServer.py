import socket
import select

class ChatServer:
    def __init__ (self, port):
        self.port = port;
        self.srvsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srvsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.srvsock.bind( ("", port) )
        self.srvsock.listen(5)
        self.descriptors = [self.srvsock]
        print 'CharServer started on port %s' % port
    def run(self):
        while True:
            #Await an event on a readable socket descriptor
            sread,swrite,sexc = select.select(self.descriptors, [], [])
            #Iterate through the tagged read descriptors
            for sock in sread:
                #Receieved a connect to the server socket
                if sock == self.srvsock:
                    self.accept_new_connection()
                else:
                    str = sock.recv(100)
                    if str == '':
                        host,port = sock.getpeername()
                        str = 'Client left %s: %s \r\n' %(host, port)
                        self.broadcast_string(str, sock)
                        sock.closer
                        self.descriptors.remove(sock)
                    else:
                        host,port = sock.getpeername()
                        newstr = '[%s,%s] %s' %(host,port, str)
                        self.broadcast_string(newstr, sock)

    def accept_new_connection(self):
        newsock, (remhost, remport) = self.srvsock.accept()
        self.descriptors.append(newsock)
        newsock.send("you are connected to the python chatserver\r\n")
        str = 'Client joined %s: %s\r\n' % (remhost, remport)
        self.broadcast_string(str,newsock)

    def broadcast_string(self, str, omit_sock):
        for sock in self.descriptors:
            if sock != self.srvsock and sock != omit_sock:
                sock.send(str)
            print(str)

myServer = ChatServer(8000)
myServer.run()
