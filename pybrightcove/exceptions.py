class BrightcoveClientError(Exception):
    pass


class BrightcoveGeneralError(Exception):
    code = None
    message = None
    data = None
    
    def __iniit__(self, code, message, data):
        self.code = code
        self.message = message
        self.data = data


class BrightcoveError(Exception):
    error = None
    code  = None
    
    def __init__(self, data):
        self.error = data['error']
        self.code  = data['code']