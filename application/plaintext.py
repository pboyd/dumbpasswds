from .error import UserError

class PlainText:
    rules = [ 'Must have between 8 and 16 characters' ]
    code = "plaintext"
    name = "Plain-Text"

    schema = '''
    CREATE TABLE plaintext (
        username text PRIMARY KEY,
        password text
    )
    '''

    def login(self, cursor, username, password):
        cursor.execute("SELECT count(*) FROM plaintext WHERE username='%s' AND password='%s'" % (username, password))
        result = cursor.fetchone()
        if result[0] == 0:
            raise UserError("Invalid username or password")
