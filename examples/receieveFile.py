from pysocks.src.Socket import UDPSocket

newSocket = UDPSocket(recv_port=4443, socket_type='receiver')
newSocket.receiveData(write_to_file=True, file_name='testing_image.jpeg', encoding='base64')
newSocket.clearSockets()