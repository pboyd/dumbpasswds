from .plaintext import PlainText
from .encrypted import Encrypted
from .md5 import MD5
from .sha256 import SHA256
from .salted_md5 import SaltedMD5
from .salted_sha256 import SaltedSHA256
from .scrypt import Scrypt
from .argon2i import Argon2i

AllTypes = [
        PlainText,
        Encrypted,
        MD5,
        SHA256,
        SaltedMD5,
        SaltedSHA256,
        Scrypt,
        Argon2i,
]

AllTypesDict = {}
for t in AllTypes:
    AllTypesDict[t.code] = t
