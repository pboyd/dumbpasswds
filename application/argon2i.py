from .error import UserError

import nacl.pwhash
import secrets

class Argon2i:
    code = "argon2i"
    name = "Argon2i"

    schema = '''
    CREATE TABLE IF NOT EXISTS argon2i (
        username VARCHAR(16) PRIMARY KEY,
        password VARCHAR(160)
    )
    '''

    def login(self, cursor, username, password):
        cursor.execute("SELECT password FROM argon2i WHERE username=%s", (username,))
        result = cursor.fetchone()
        if result == None:
            raise UserError("Invalid username or password.")

        if not self.check_password(result[0], password):
            raise UserError("Invalid username or password.")

    def create_account(self, cursor, username, password):
        if len(password) < 8:
            raise UserError("Password must contain more than 8 characters.")

        cursor.execute("SELECT count(*) FROM argon2i WHERE username=%s", (username,))
        result = cursor.fetchone()
        if result[0] > 0:
            raise UserError("Username already taken.")

        hashed = self.hash_password(password)
        cursor.execute("INSERT INTO argon2i (username, password) VALUES (%s, %s)", (username, hashed))

    def hash_password(self, password, salt=None):
        if salt == None:
            salt = secrets.token_bytes(16)

        hashed = nacl.pwhash.argon2i.kdf(64, bytes(password, 'utf-8'), salt)
        return salt.hex() + hashed.hex()

    def check_password(self, hashed, password):
        salt = bytes.fromhex(hashed[0:32])
        new_hashed = self.hash_password(password, salt)
        return new_hashed == hashed
