from socket import *
from codecs import decode
from time import ctime,sleep
from threading import Thread,currentThread,Condition
host='localhost'
port=5000
buffsize=1024
ADDRESS=(host,port)

server=socket(AF_INET,SOCK_STREAM)
server.bind(ADDRESS)
server.listen(5)
while True:
    print("waiting for a connection....")
    client,address=server.accept()
    print("....connected from: ",address)
    client.send(bytes("Username: ",'ascii'))
    msg=decode(client.recv(buffsize),'ascii')
    handler=chatthread(client,msg)
    handler.start()


class chatthread(Thread):
    def __init__(self,client,msg):
        Thread.__init__(self)
        self._cell=sharedcell()
        self._client=client
        self._msg=msg
    def run(self):
        self._greet()
        self._getdata()
        while True:
            mesg=decode(self._client.recv(buffsize),'ascii')
            self._cell.setdata(self._msg+" "+ctime()+"\n"+mesg)
            self._client.send(bytes(
        
    def greet(self):
        return "welcome back "+currentThread().getName()
    def _getdata(self):
        return self._cell._data
    
class sharedcell(object):
    def __init__(self):
        self._writeable=True
        self._condition=Condition()
        self._data=[]
    def setData(self,data):
        self._condition.acquire()
        while not self._writeable:
            self._condition.wait()
        self._data.append(data)
        self._writeable=False
        self._condition.notify()
        self._condition.release()
    def getData(self):
        self._condition.acquire()
        while self._writeable:
            self._condition.wait()
        self.string()
        self._writeable=True
        self._condition.notify()
        self._condition.release()
    def string(self):
        if len(self._data)==0:
            return "no messages yet"
        else:
            return "\n".join(self._data)
