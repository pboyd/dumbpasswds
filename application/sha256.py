from .error import UserError

import hashlib

class SHA256:
    code = "sha256"
    name = "SHA256"

    schema = '''
    CREATE TABLE IF NOT EXISTS sha256 (
        username VARCHAR(16) PRIMARY KEY,
        password VARCHAR(64)
    )
    '''

    def login(self, cursor, username, password):
        cursor.execute("SELECT password FROM sha256 WHERE username=%s", (username,))
        result = cursor.fetchone()
        if result == None:
            raise UserError("Invalid username or password.")

        if result[0] != self.hash_password(password):
            raise UserError("Invalid username or password.")

    def create_account(self, cursor, username, password):
        if len(password) < 8:
            raise UserError("Password must contain more than 8 characters.")

        cursor.execute("SELECT count(*) FROM sha256 WHERE username=%s", (username,))
        result = cursor.fetchone()
        if result[0] > 0:
            raise UserError("Username already taken.")

        hashed = self.hash_password(password)
        cursor.execute("INSERT INTO sha256 (username, password) VALUES (%s, %s)", (username, hashed))

    def hash_password(self, password):
        return hashlib.sha256(bytes(password, 'utf-8')).hexdigest()
