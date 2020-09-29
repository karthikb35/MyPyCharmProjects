from user import User
from AuthExceptions import AuthException,PasswordTooShort, UsernameAlreadyExisits

class Authenticator:
    global UserList
    def authenticate( self,username, password ):
        for user in UserList.userlist:
            if username == user.username:
                return user.checkPassword(password)
        return False

class userList:
    def __init__(self):
        self.userlist = []

    def addUser( self,username, password ):
        if username in [user.username for user in self.userlist] :
            raise UsernameAlreadyExisits(f'{username} already exists')
        if len(password) < 3:
            raise PasswordTooShort('Password too short')
        self.userlist.append(User(username, password))

UserList = userList()

class Menu:
    global UserList

    def __init__(self):
        self.authenticator = Authenticator()

    def adduser( self ):
        username = input("Enter Username")
        password = input("Enter password")
        UserList.addUser(username,password)

    def authenticate( self ):
        username = input ( "Enter Username" )
        password = input ( "Enter password" )
        if self.authenticator.authenticate(username,password):
            print("User valid")
        else:
            print("User invalid!!")

    def menu( self ):
        menu_actions = {
            "1": self.adduser,
            "2": self.authenticate,
            "3": exit
        }
        while True:
            action = input(
                "1. Add User\n"
                "2. Authenticate user\n"
                "3. Exit\n"
            )
            menu_actions[action]()

Menu().menu()