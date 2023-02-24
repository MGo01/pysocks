from pysocks.src.Socket import UDPSocket
from pysocks.src.message import FileMessage

# Use the full file path for now
# to create the message
newMessage = FileMessage(file_name='/Users/mattgomez/Desktop/git/python-projects/pysocks/testFiles/jpg/colorful_art.jpeg')
newMessage.createMessage()

newSocket = UDPSocket(send_port=4443, socket_type='sender')

newSocket.sendData(newMessage)

newSocket.stopSending(encoding='utf-8')
newSocket.clearSockets()