import json
import yaml
import base64
from message_config import file_types, serial_types

"""
Base class for all Messages
"""
class Message:

    def __init__(self, file_type=None, serial_type=None, data=None, encoding_type='utf-8'):

        header = {}

        header['file-type'] = file_type
        header['encoding-type'] = encoding_type
        header['serial-type'] = serial_type

        self.file_type = file_type
        self.serial_type = serial_type
        self.header = header
        self.payload = None
    

    def isAllowedFileType(self, file_type: str) -> bool:
        return file_type in file_types

    
    def isAllowedSerialType(self, serial_type: str) -> bool:
        return serial_type in serial_types


    def _createMessage(self):
        pass


    def deleteMessage(self):

        self.header = None
        self.payload = None
        self.file_type = None
        self.serial_type = None


    def printDebugInfo(self, data):

        debugString = (
            f"Debug String\n"
            f"============\n"
            f"Header: {self.header}"
            f"Data: {self.payload}\n"
        )

        print(debugString)

"""
Receieves a serialized message in the form
of a dictionary and converts it into JSON or YAML
"""
class SerialMessage(Message):

    def __init__(self, file_type=None, serial_type=None, data=None, encoding_type='utf-8'):
        
        if not self.isAllowedSerialType(serial_type):
            raise Exception(f"Serial type, {serial_type} not allowed")
        
        if not isinstance(data, dict):
            raise Exception(f"Incorrect Data type: {type(data)} not allowed, use a dictionary instead")
        
        super().__init__(file_type, serial_type, data, encoding_type)

    def _createMessage(self):

        encodedData = None

        if self.serial_type == 'json':
            encodedData = json.dumps(self.data).encode(self.encoding_type)
            self.payload = encodedData
        
        if self.serial_type == 'yml' or self.serial_type == 'yml':
            encodedData = yaml.dumps(self.data).encode(self.encoding_type)
            self.payload = encodedData

"""
Receieves the name of a file
and converts it into a base64 string
"""
class FileMessage(Message):

    def __init__(self, file_type=None, serial_type=None, data=None, file_name='', encoding_type='base64'):

        if file_name.count('.') > 1:
            raise Exception(f"Too many periods in file name: {file_name}")

        trash, file_type  = file_name.split('.')
        self.file_name = file_name

        if not self.isAllowedFileType(file_type):
            raise Exception(f"File type, {file_type} not allowed")

        super().__init__(file_type, serial_type, data, encoding_type)


    def _createMessage(self):

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
        
        if self.file_type == 'yaml' or self.file_type == 'yml':
            # Opening YML file
            inputFile = open(self.file_name)
            
            # returns YML key, value pairs 
            # as a dictionary
            dataDict = yaml.safe_load(inputFile)
            encodedData = yaml.dumps(dataDict).encode(self.encoding_type)
            self.payload = encodedData

        if self.file_name != '':
            inputFile = open(self.file_name, 'rb')
            file_content = inputFile.read()

            encodedData = base64.encodestring(file_content)
            self.payload = encodedData
        

        self.header['length'] = len(encodedData)
        inputFile.close()