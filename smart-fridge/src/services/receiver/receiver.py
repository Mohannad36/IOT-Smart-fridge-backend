import socket

from queue import LifoQueue

from threading import Thread

class Message:
    def __init__(self,
                 data) -> None:
        self.data: str = data
        self.headers: dict = {}
        self.create()

    def create(self) -> None:
        headersStart: int = self.data.find("<")
        headersEnd: int   = self.data.find(">")
        if headersStart != -1 and headersEnd != -1:
            tmpData: str = self.data[headersStart+1:headersEnd]
            headerTags = tmpData.split(";")
            for tag in headerTags:
                tag = tag.split("=")
                if len(tag) == 2:
                    self.headers[tag[0]] = tag[1]
        self.data = self.data[headersEnd+1:]


class ServerConnectionHandler(Thread):
    inData: LifoQueue = LifoQueue()
    def __init__(self,
                 connection: socket,
                 address: str,
                 packetReadMaxSize: int = 1024):
        Thread.__init__(self)
        self.daemon = True

        self.connection = connection
        self.address = address
        self.maxReadPerPacketInBytes = packetReadMaxSize

    def run(self):
        dataHandler = Thread(target = self.interpretData, daemon=True)
        dataHandler.start()
        while True:
            self.receive()

    def receive(self):
        data: str = self.connection.recv(self.maxReadPerPacketInBytes)
        if data:
            buffer: str = ""
            buffer += data.decode()
            while not buffer.endswith("<END>"):
                buffer += self.connection.recv(self.maxReadPerPacketInBytes).decode()
            for bufferData in buffer.split("<END>"):
                if len(bufferData) > 0:
                    newMessage: Message = Message(bufferData)
                    self.inData.put(newMessage)


    def interpretData(self):
        while True:
            if not self.inData.empty():
                message = self.inData.get()
                
                print(f"[/] Received Data :: {message.data} . . .")
                for tag, value in message.headers.items():
                    print(f"[/] Received Tag :: {tag} with a value of {value} . . .")
                print("")

                self.inData.task_done()
            
        
class ServerSocket:
    def __init__(self, 
                 host: str = "0.0.0.0", port: int = 12444,
                 localHost: str = "127.0.0.1", localPort: int = 12445) -> None:
        self.receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receiver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        self.host = host
        self.port = port

        self.localHost = localHost
        self.localPort = localPort

        self.clients = []

    def handleNewConnection(self) -> None:
        clientSocket, address = self.receiver.accept()
        
        print(f"[+] Received new connection on {address} . . .\n")

        receiver: ServerConnectionHandler = ServerConnectionHandler(clientSocket, address)
        self.clients.append(receiver)
        receiver.start()

    def start(self,
              maxConnections: int) -> None:
        self.receiver.bind((self.host, self.port))
        self.receiver.listen(maxConnections)

        print(f"[+] Server bound to {self.host}:{self.port} . . .")
        while True:
            self.handleNewConnection()


def main() -> None:
    server: ServerSocket = ServerSocket()
    server.start(5)

if __name__ == "__main__":
    main()
