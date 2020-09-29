import hashlib

class User:
    def __init__(self, username, password):
        self.username = username
        self.isLoggedIn = False
        self.password = self._encPass(password)

    def _encPass( self, password ):
        hash_string = (self.username + password)
        hash_string = hash_string.encode ( "utf8" )
        return hashlib.sha256 ( hash_string ).hexdigest ( )

    def checkPassword( self, password ):
        return self._encPass(password) == self.password

