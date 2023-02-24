import json
import base64
import struct
from .message_config import file_types, serial_types, format_char_types, byte_order_types

"""
Base class for all Messages
"""
class Message:

    def __init__(self, endianness, msg_format, serial_type=None, data=None, encoding_type='utf-8'):

        header = {}
        header['encoding-type'] = encoding_type
        header['serial-type'] = serial_type
        header['']

        self.serial_type = serial_type
        self.encoding_type = encoding_type
        self.header = header
        self.data = data
        self.payload = None
    

    def isAllowedFileType(self, file_type: str) -> bool:
        return file_type in file_types

    
    def isAllowedSerialType(self, serial_type: str) -> bool:
        return serial_type in serial_types


    def isAllowedFormatCharType(self, format_char: str) -> bool:
        return format_char in format_char_types
    

    def isAllowedByteOrderType(self, byte_order_type: str) -> bool:
        return byte_order_type in byte_order_type


    def createMessage(self):
        pass


    def deleteMessage(self):

        self.header = None
        self.payload = None
        self.file_type = None
        self.serial_type = None
    

    def getMessage(self) -> bytes:
        return self.payload

    
    def decodeMessage(self) -> any:
        
        if self.file_type is None:
            raise Exception('Null file type detected in decodeMessage()')
        
        if self.serial_type is None:
            raise Exception('Null serial type detected in decodeMessage()')
        
        if self.encoding_type is None:
            raise Exception('Null encoding type detected in decodeMessage()')

        if not isinstance(self.payload, bytes):
            raise Exception('Payload must be a byte array before decoding')

        if self.encoding_type == 'utf-8':
            return self.payload.decode(self.encoding_type)

        elif self.encoding_type == 'base64':
            return base64.b64decode(self.payload)
        else:
            return self.payload.decode(self.encoding_type)


    def printDebugInfo(self):

        debugString = (
            f"Debug String\n"
            f"============\n"
            f"Header: {self.header}"
            f"Data: {self.payload}\n"
        )

        print(debugString)

"""
Receieves a serialized message in the form
of a dictionary and converts it into JSON
"""
class SerialMessage(Message):

    def __init__(self, data, serial_type=None, encoding_type='utf-8'):
        
        if not self.isAllowedSerialType(serial_type):
            raise Exception(f"Serial type, {serial_type} not allowed")
        
        if not isinstance(data, dict):
            raise Exception(f"Incorrect Data type: {type(data)} not allowed, use a dictionary instead")
        
        super().__init__(serial_type, data, encoding_type)


    def createMessage(self):

        if self.serial_type == 'json':
            encodedData = json.dumps(self.data).encode(self.encoding_type)
            self.payload = encodedData
    

    def decodeMessage(self):
        return super().decodeMessage()


"""
Receieves the name of a file
and converts it into a base64 string
"""
class FileMessage(Message):

    def __init__(self, file_name, serial_type=None, data=None, encoding_type='base64'):

        if file_name.count('.') > 1:
            raise Exception(f"Too many periods in file name: {file_name}")

        trash, file_type  = file_name.split('.')

        if not self.isAllowedFileType(file_type):
            raise Exception(f"File type, {file_type} not allowed")

        self.file_type = file_type
        self.file_name = file_name

        super().__init__(serial_type, data, encoding_type)


    def createMessage(self):

        encodedData = None
        inputFile = None

        if self.file_type == 'json':
            # Opening JSON file
            inputFile = open(self.file_name)
            
            # returns JSON object as 
            # a dictionary then encodes the
            # dictionary as a byte string
            dataDict = json.load(inputFile)
            encodedData = json.dumps(dataDict).encode(self.encoding_type)
            self.payload = encodedData

        elif self.file_name != '':
            inputFile = open(self.file_name, 'rb')
            file_content = inputFile.read()

            encodedData = base64.encodestring(file_content)
            self.payload = encodedData
        
        self.header['length'] = len(encodedData)
        inputFile.close()


    def decodeMessage(self):
        return super().decodeMessage()