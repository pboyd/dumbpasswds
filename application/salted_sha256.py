from .error import UsernameTaken, BadLogin, PasswordTooShort

import hashlib
import secrets

class SaltedSHA256:
    code = "salted_sha256"
    name = "Salted SHA256"

    schema = '''
    CREATE TABLE IF NOT EXISTS salted_sha256 (
        username VARCHAR(16) PRIMARY KEY,
        password VARCHAR(96)
    )
    '''

    def login(self, cursor, username, password):
        cursor.execute("SELECT password FROM salted_sha256 WHERE username=%s", (username,))
        result = cursor.fetchone()
        if result == None:
            raise BadLogin()

        if not self.check_password(result[0], password):
            raise BadLogin()

    def create_account(self, cursor, username, password):
        if len(password) < 8:
            raise PasswordTooShort()

        cursor.execute("SELECT count(*) FROM salted_sha256 WHERE username=%s", (username,))
        result = cursor.fetchone()
        if result[0] > 0:
            raise UsernameTaken()

        hashed = self.hash_password(password)
        cursor.execute("INSERT INTO salted_sha256 (username, password) VALUES (%s, %s)", (username, hashed))

    def hash_password(self, password, salt=None):
        if salt == None:
            salt = secrets.token_bytes(16)

        salted_password = salt + bytes(password, 'utf-8')
        return salt.hex() + hashlib.sha256(salted_password).hexdigest()

    def check_password(self, hashed, password):
        salt = bytes.fromhex(hashed[0:32])
        new_hashed = self.hash_password(password, salt)
        return new_hashed == hashed
