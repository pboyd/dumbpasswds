class UserError(Exception):
    def __init__(self, message):
        self.message = message

class BadLogin(UserError):
    def __init__(self):
        super(BadLogin, self).__init__("Invalid username or password.")

class UsernameTaken(UserError):
    def __init__(self):
        super(UsernameTaken, self).__init__("Username already taken.")

class PasswordTooShort(UserError):
    def __init__(self, min=8):
        super(PasswordTooShort, self).__init__("Password must contain more than %d characters." % (min))

class PasswordTooLong(UserError):
    def __init__(self, max=16):
        super(PasswordTooLong, self).__init__("Password must contain fewer than %d characters." % (max))
