import base64


class Authentication (object):
    def __init__ (self, master_key, parser_credentials):
        self.master_key = master_key
        self.parser_credentials = parser_credentials

    def encode(self, key, string):
        encoded_chars = []

        for i in range(len(string)):
            key_c = key[i % len(key)]
            encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
            encoded_chars.append(encoded_c)

        encoded_string = "".join(encoded_chars)
        return encoded_string

    def decode(self, key, string):
        encoded_chars = []

        for i in range(len(string)):
            key_c = key[i % len(key)]
            encoded_c = chr(ord(string[i]) - ord(key_c) % 256)
            encoded_chars.append(encoded_c)

        encoded_string = "".join(encoded_chars)
        return encoded_string

    def auth (self, app_credentials):
        if app_credentials == self.parser_credentials:
            return True
        else:
            return False

    def is_auth (self, credentials):
        decoded = self.decode(self.master_key, credentials)
        data = decoded.split("__")
        req_credential = {data[0]:data[1]}
        is_auth = self.auth(req_credential)
        return is_auth


