from abc import ABC
class resp_type(ABC):
    def __init__(self, message):
        """Initialize the RESP object"""
    
    def serialize(self):
        """Convert the object into RESP protocol strings"""

class SimpleString(resp_type):
    def __init__(self, message):
        self.s = message[1:-2]

    def serialize(self):
        return f"+{self.s}\r\n"
    
    def getString(self):
        return self.s

class Error(resp_type):
    def __init__(self, message):
        self.err = message[1:-2]

    def serialize(self):
        return f"-{self.err}\r\n"
    
    def getError(self):
        return self.err

class Integer(resp_type):
    def __init__(self, message):
        self.num = int(message[1:-2])

    def serialize(self):
        return f":{self.num}\r\n"
    
    def getInteger(self):
        return self.num

class BulkString(resp_type):
    def __init__(self, message):
        self.bytes = int(message.split('\r\n')[0][1:])
        if self.bytes == -1:
            self.val = None
        else:
            self.val = message[4:4+bytes]

    def serialize(self):
        if self.val is None:
            return "$-1\r\n"
        return f"${self.bytes}\r\n{self.val}\r\n"
    def getString(self):
        return self.val

class Array(resp_type):
    def __init__(self, message):
        self.length = int(message.split('\r\n')[0][1:])
        self.arr = []
        for i in range()


    def serialize(self):
        pass