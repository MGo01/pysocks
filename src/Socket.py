import time
import socket
from .socket_config import allowed_types
from .message import Message, SerialMessage, FileMessage

MILLISECONDS = 0.001

class Socket:

    def __init__(self, recv_port=None, send_port=None, bind_addr='', send_addr='localhost', socket_type='', buffer_size=1024):
        
        if not self.isAllowedType(socket_type):
            raise Exception(f"Socket type, {socket_type} not allowed")

        self.recv_socket = None
        self.send_socket = None
        self.buffer_size = buffer_size
        self.socket_type = socket_type

        if socket_type == 'receiver':
            self.recv_port = recv_port
            self.bind_addr = bind_addr
        
        elif socket_type == 'sender':
            self.send_port = send_port
            self.send_addr = send_addr
        else:
            self.recv_port = recv_port
            self.send_port = send_port
            self.bind_addr = bind_addr
            self.send_addr = send_addr
    

    def isAllowedType(self, socket_type: str) -> bool:
        return socket_type in allowed_types


    def _createReceiverSocket(self):
        pass


    def _createSenderSocket(self):
        pass


    def clearSockets(self):

        if self.socket_type == 'receiver':
            self.recv_socket.close()
            self.recv_socket = None
        
        elif self.socket_type == 'sender':
            self.send_socket.close()
            self.send_socket = None
        else:
            self.recv_socket.close()
            self.recv_socket = None
            self.send_socket.close()
            self.send_socket = None


    def _sendData(self, byteString, delayMS):
        time.sleep(delayMS * MILLISECONDS)
        self.send_socket.sendall(byteString)


    def stopSending(self, delayMS=10, encoding=None):
        finalMessage = '#DONE#'
        time.sleep(delayMS * MILLISECONDS)
        self.send_socket.send(finalMessage.encode(encoding))


    def isFinishedSending(self, data):
        return data == '#DONE#'


    def isMessage(self, data):
        return isinstance(data, Message)


    def sendData(self, data=None, delayMS=10):
        
        if self.send_socket is None:
            raise Exception('Null Sending Socket detected')

        if not self.isMessage(data):
            raise Exception('Data is not an instance of the Message class, use the Message class')

        self._sendData(data.getMessage(), delayMS)


    def printDebugInfo(self, data):

        debugString = (
            f"Debug String\n"
            f"Data: {data}\n"
        )

        print(debugString)


    def receiveData(self, write_to_file=False, file_name=None, encoding='utf-8', callback=None):
        
        if self.recv_socket is None:
            raise Exception('Null Receiver Socket detected in receiveData()')

        elif write_to_file and file_name is not None:
            chunk = None
            outputFile = open(file_name, 'wb')

            while True:
                chunk = self.recv_socket.recv(self.buffer_size)
                decodedChunk = chunk.decode(encoding)

                if self.isFinishedSending(decodedChunk):
                    break

                outputFile.write(decodedChunk)
        else:
            chunk = None

            while True:
                chunk = self.recv_socket.recv(self.buffer_size)
                decodedChunk = chunk.decode(encoding)

                if self.isFinishedSending(decodedChunk):
                    break

                if callback is None:
                    self.printDebugInfo(decodedChunk)
                else:
                    callback(decodedChunk)


class UDPSocket(Socket):

    def __init__(self, recv_port=None, send_port=None, bind_addr='', send_addr='localhost', socket_type='', buffer_size=1024):
        
        super().__init__(recv_port, send_port, bind_addr, send_addr, socket_type, buffer_size)

        if socket_type == 'receiver':
            self.recv_socket = self._createReceiverSocket()
        
        elif socket_type == 'sender':
            self.send_socket = self._createSenderSocket()
        
        else:
            self.recv_socket = self._createReceiverSocket()
            self.send_socket = self._createSenderSocket()
    

    def _createReceiverSocket(self):
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        recv_socket.bind((self.bind_addr, self.recv_port))

        return recv_socket


    def _createSenderSocket(self):
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        send_socket.connect((self.send_addr, self.send_port))

        return send_socket


class TCPSocket(Socket):

    def __init__(self, recv_port=None, send_port=None, bind_addr='', send_addr='localhost', socket_type='', buffer_size=1024, listeners=1):
        
        super().__init__(recv_port, send_port, bind_addr, send_addr, socket_type, buffer_size)

        if socket_type == 'receiver':
            self.recv_socket = self._createReceiverSocket()
        
        elif socket_type == 'sender':
            self.send_socket = self._createSenderSocket()
        
        else:
            self.recv_socket = self._createReceiverSocket()
            self.send_socket = self._createSenderSocket()
        
        self.listeners = listeners
    

    def _createReceiverSocket(self):
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        recv_socket.bind((self.bind_addr, self.recv_port))
        recv_socket.listen(self.listeners)

        return recv_socket


    def _createSenderSocket(self):
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        send_socket.connect((self.send_addr, self.send_port))

        return send_socket
    

    def acceptConnection(self):

        if self.recv_socket is None:
            raise Exception('Null Receiver Socket detected in acceptConnection()')

        connection, client_address = self.recv_socket.accept()
        self.recv_socket = connection
