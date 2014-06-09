__author__ = 'pavel'

import  socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005



def UP(self, L, R, U,P):
    #self.MESSAGE = L, R, U, P

   # self.sock = socket.socket( socket.AF_INET,
                        #        socket.SOCK_DGRAM)
    #self.sock.sendto( self.MESSAGE, (UDP_IP, UDP_PORT))


    sock = socket.socket( socket.AF_INET, # Internet
                      socket.SOCK_DGRAM ) # UDP
    sock.sendto( bytes(L, R, U, P, "utf-8"),(UDP_IP, UDP_PORT) )



def DOWN():
    #pass
    sock = socket.socket( socket.AF_INET, # Internet
                      socket.SOCK_DGRAM ) # UDP
    sock.bind( (UDP_IP,UDP_PORT) )
    data, addr = sock.recvfrom( 1024 ) # buffer size is 1024 bytes
    return  data.decode("utf-8")


