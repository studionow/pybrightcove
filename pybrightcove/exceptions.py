class BrigthcoveClientError(Exception):
    pass


class BrightcoveGeneralError(Exception):
    self.code = None
    self.message = None
    self.data = None
    
    def __iniit__(self, code, message, data):
        self.code = code
        self.message = message
        self.data = data


class BrightcoveError(Exception):
    self.error = None
    self.code  = None
    
    def __init__(self, data):
        self.error = data['error']
        self.code  = data['code']