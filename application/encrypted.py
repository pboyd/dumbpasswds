from .error import UsernameTaken, BadLogin, PasswordTooShort, PasswordTooLong

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
            raise BadLogin()

        decrypted = self.decrypt_password(result[0])
        if decrypted != password:
            raise BadLogin()

    def create_account(self, cursor, username, password):
        if len(password) < 8:
            raise PasswordTooShort()

        if len(password) > 16:
            raise PasswordTooLong()

        cursor.execute("SELECT count(*) FROM encrypted WHERE username=%s", (username,))
        result = cursor.fetchone()
        if result[0] > 0:
            raise UsernameTaken()

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
