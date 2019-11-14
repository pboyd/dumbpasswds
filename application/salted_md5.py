from .error import UsernameTaken, BadLogin, PasswordTooShort

import hashlib
import secrets

class SaltedMD5:
    code = "salted_md5"
    name = "Salted MD5"

    schema = '''
    CREATE TABLE IF NOT EXISTS salted_md5 (
        username VARCHAR(16) PRIMARY KEY,
        password VARCHAR(48)
    )
    '''

    def login(self, cursor, username, password):
        cursor.execute("SELECT password FROM salted_md5 WHERE username=%s", (username,))
        result = cursor.fetchone()
        if result == None:
            raise BadLogin()

        if not self.check_password(result[0], password):
            raise BadLogin()

    def create_account(self, cursor, username, password):
        if len(password) < 8:
            raise PasswordTooShort()

        cursor.execute("SELECT count(*) FROM salted_md5 WHERE username=%s", (username,))
        result = cursor.fetchone()
        if result[0] > 0:
            raise UsernameTaken()

        hashed = self.hash_password(password)
        cursor.execute("INSERT INTO salted_md5 (username, password) VALUES (%s, %s)", (username, hashed))

    def hash_password(self, password, salt=None):
        if salt == None:
            salt = secrets.token_bytes(8)

        salted_password = salt + bytes(password, 'utf-8')
        return salt.hex() + hashlib.md5(salted_password).hexdigest()

    def check_password(self, hashed, password):
        salt = bytes.fromhex(hashed[0:16])
        new_hashed = self.hash_password(password, salt)
        return new_hashed == hashed
