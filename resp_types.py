from abc import ABC

class RespType(ABC):
    def __init__(self, message, index):
        """Initialize the RESP object"""
    
    def getIndex(self):
        """Return the index after done parsing this message"""

    def serialize(self):
        """Convert the object into RESP protocol strings"""

class SimpleString(RespType):
    def __init__(self, message, index=None):
        if index  is None:
            self.s = message
            self.index = None
        else:
            endLine = message.find('\r\n', index)
            self.s = message[index+1:endLine]
            self.index = endLine + 2
    
    def __len__(self):
        return len(self.s)
    
    def __getitem__(self, ind):
        return self.s[ind]

    def __repr__(self) -> str:
        return self.s

    def serialize(self):
        return f"+{self.s}\r\n"
    
    def getString(self):
        return self.s
    
    def getIndex(self):
        return self.index

class Error(RespType):
    def __init__(self, message, index):
        endLine = message.find('\r\n', index)
        self.err = message[index+1:endLine]
        self.index = endLine + 2

    def __repr__(self):
        return self.err

    def serialize(self):
        return f"-{self.err}\r\n"
    
    def getError(self):
        return self.err
    
    def getIndex(self):
        return self.index

class Integer(RespType):
    def __init__(self, message, index):
        endLine = message.find('\r\n', index)
        self.num = int(message[index+1:endLine])
        self.index = endLine + 2

    def __repr__(self) -> str:
        return str(self.num)

    def serialize(self):
        return f":{self.num}\r\n"
    
    def getInteger(self):
        return self.num
    
    def getIndex(self):
        return self.index

class BulkString(RespType):
    def __init__(self, message, index):
        endLine = message.find('\r\n', index)
        self.bytes = int(message[index+1:endLine])

        if self.bytes == -1:
            self.val = None
            self.index = endLine + 2
        else:
            offset = endLine + 2 #read $
            self.val = message[offset:offset + self.bytes]
            self.index = offset + self.bytes + 2

    def __len__(self):
        return self.bytes
    
    def __repr__(self):
        return self.val
    
    def serialize(self):
        if self.val is None:
            return "$-1\r\n"
        else:
            return f"${self.bytes}\r\n{self.val}\r\n"
    
    def getString(self):
        return self.val
    
    def getIndex(self):
        return self.index

class Array(RespType):
    def __init__(self, message, index):
        lineEnd = message.find('\r\n', index)
        numElements = int(message[index+1:lineEnd])
        index = lineEnd + 2 # go past \r\n

        parsedElements = 0
        elements = []

        while index < len(message) and parsedElements < numElements:
            data_type = message[index]
            match data_type:
                case '+':
                    s = SimpleString(message, index)
                    elements.append(s)
                    parsedElements += 1
                    index = s.getIndex()

                case '-':
                    e = Error(message, index)
                    elements.append(e)
                    parsedElements += 1
                    index = e.getIndex()

                case ':':
                    i = Integer(message, index)
                    elements.append(i)
                    parsedElements += 1
                    index = i.getIndex()

                case '$':
                    bs = BulkString(message, index)
                    elements.append(bs)
                    parsedElements += 1
                    index = bs.getIndex()

                case '*':
                    arr = Array(message, index)
                    elements.append(arr)
                    parsedElements += 1
                    index = arr.getIndex()

                case _:
                    raise ValueError(f'Could not parse {message}')
        self.index = index
        self.arr = elements
    
    def __len__(self):
        return len(self.arr)
    
    def __getitem__(self, ind):
        return self.arr[ind]
    
    def __repr__(self):
        return str(self.arr)
    
    def __str__(self):
        return str(self.arr)

    def getArray(self):
        return self.arr

    def getIndex(self):
        return self.index

    def serialize(self):
        s = f'*{len(self)}\r\n'
        for i in range(len(self)):
            s += self[i].serialize()
        return s