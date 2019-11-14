from .error import UserError

class PlainText:
    code = "plaintext"
    name = "Plain Text"

    schema = '''
    CREATE TABLE IF NOT EXISTS plaintext (
        username VARCHAR(16) PRIMARY KEY,
        password VARCHAR(16)
    )
    '''

    def login(self, cursor, username, password):
        cursor.execute("SELECT count(*) FROM plaintext WHERE username=%s AND password=%s", (username, password))
        result = cursor.fetchone()
        if result[0] == 0:
            raise UserError("Invalid username or password.")

    def create_account(self, cursor, username, password):
        if len(password) < 8:
            raise UserError("Password must contain more than 8 characters.")

        if len(password) > 16:
            raise UserError("Password must contain fewer than 16 characters.")

        cursor.execute("SELECT count(*) FROM plaintext WHERE username=%s", (username,))
        result = cursor.fetchone()
        if result[0] > 0:
            raise UserError("Username already taken.")

        cursor.execute("INSERT INTO plaintext (username, password) VALUES (%s, %s)", (username, password))
