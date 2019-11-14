from .error import UsernameTaken, BadLogin, PasswordTooShort

import hashlib

class MD5:
    code = "md5"
    name = "MD5"

    schema = '''
    CREATE TABLE IF NOT EXISTS md5 (
        username VARCHAR(16) PRIMARY KEY,
        password VARCHAR(32)
    )
    '''

    def login(self, cursor, username, password):
        cursor.execute("SELECT password FROM md5 WHERE username=%s", (username,))
        result = cursor.fetchone()
        if result == None:
            raise BadLogin()

        if result[0] != self.hash_password(password):
            raise BadLogin()

    def create_account(self, cursor, username, password):
        if len(password) < 8:
            raise PasswordTooShort()

        cursor.execute("SELECT count(*) FROM md5 WHERE username=%s", (username,))
        result = cursor.fetchone()
        if result[0] > 0:
            raise UsernameTaken()

        hashed = self.hash_password(password)
        cursor.execute("INSERT INTO md5 (username, password) VALUES (%s, %s)", (username, hashed))

    def hash_password(self, password):
        return hashlib.md5(bytes(password, 'utf-8')).hexdigest()
