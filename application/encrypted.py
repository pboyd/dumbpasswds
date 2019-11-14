from .error import UserError

import nacl.secret

class Encrypted:
    code = "encrypted"
    name = "Encrypted"

    schema = '''
    CREATE TABLE IF NOT EXISTS encrypted (
        username VARCHAR(16) PRIMARY KEY,
        password VARCHAR(120)
    )
    '''

    def login(self, cursor, username, password):
        cursor.execute("SELECT password FROM encrypted WHERE username=%s", (username,))
        result = cursor.fetchone()
        if result == None:
            raise UserError("Invalid username or password.")

        decrypted = self.decrypt_password(result[0])
        if decrypted != password:
            raise UserError("Invalid username or password.")

    def create_account(self, cursor, username, password):
        if len(password) < 8:
            raise UserError("Password must contain more than 8 characters.")

        if len(password) > 16:
            raise UserError("Password must contain fewer than 16 characters.")

        cursor.execute("SELECT count(*) FROM encrypted WHERE username=%s", (username,))
        result = cursor.fetchone()
        if result[0] > 0:
            raise UserError("Username already taken.")

        encrypted = self.encrypt_password(password)
        cursor.execute("INSERT INTO encrypted (username, password) VALUES (%s, %s)", (username, encrypted))

    key = b'this is a super-duper secret key'

    def encrypt_password(self, plaintext):
        box = nacl.secret.SecretBox(self.key)
        return box.encrypt(bytes(plaintext, 'utf-8')).hex()

    def decrypt_password(self, ciphertext):
        box = nacl.secret.SecretBox(self.key)
        bc = bytes.fromhex(ciphertext)
        return box.decrypt(bc).decode('utf-8')
