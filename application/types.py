from .plaintext import PlainText
from .encrypted import Encrypted
from .hash import Hash
from .salted_hash import SaltedHash
from .scrypt import Scrypt
from .argon2i import Argon2i

AllTypes = [
        PlainText,
        Encrypted,
        Hash,
        SaltedHash,
        Scrypt,
        Argon2i,
]

AllTypesDict = {}
for t in AllTypes:
    AllTypesDict[t.code] = t
