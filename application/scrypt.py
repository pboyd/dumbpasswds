from .error import UsernameTaken, BadLogin, PasswordTooShort

import hashlib
import secrets

class Scrypt:
    code = "scrypt"
    name = "scrypt"

    schema = '''
    CREATE TABLE IF NOT EXISTS scrypt (
        username VARCHAR(16) PRIMARY KEY,
        password VARCHAR(192)
    )
    '''

    def login(self, cursor, username, password):
        cursor.execute("SELECT password FROM scrypt WHERE username=%s", (username,))
        result = cursor.fetchone()
        if result == None:
            raise BadLogin()

        if not self.check_password(result[0], password):
            raise BadLogin()

    def create_account(self, cursor, username, password):
        if len(password) < 8:
            raise PasswordTooShort()

        cursor.execute("SELECT count(*) FROM scrypt WHERE username=%s", (username,))
        result = cursor.fetchone()
        if result[0] > 0:
            raise UsernameTaken()

        hashed = self.hash_password(password)
        cursor.execute("INSERT INTO scrypt (username, password) VALUES (%s, %s)", (username, hashed))

    def hash_password(self, password, salt=None):
        if salt == None:
            salt = secrets.token_bytes(32)

        # A real implementation would use better tuning parameters.
        hashed = hashlib.scrypt(bytes(password, 'utf-8'), salt=salt, n=2**14, r=8, p=4)

        return salt.hex() + hashed.hex()

    def check_password(self, hashed, password):
        salt = bytes.fromhex(hashed[0:64])
        new_hashed = self.hash_password(password, salt)
        return new_hashed == hashed
