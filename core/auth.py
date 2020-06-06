class Authentication (object):
    def __init__ (self, MASTER, PAYLOAD):
        self.KEY = PAYLOAD.get("REACT_APP_PARSER_KEY")
        self.USER = PAYLOAD.get("REACT_APP_PARSER_USER")
        self.PASSWORD = PAYLOAD.get("REACT_APP_PARSER_PASSWORD")

        self.MASTER_KEY = MASTER.get("MASTER_KEY")
        self.MASTER_USER = MASTER.get("MASTER_USER")
        self.MASTER_PASSWORD = MASTER.get("MASTER_PASSWORD")

    
    def is_auth (self):
        if self.KEY == self.MASTER_KEY \
        and self.USER == self.MASTER_USER \
        and self.PASSWORD == self.MASTER_PASSWORD:
            return True
        else:
            return False
        