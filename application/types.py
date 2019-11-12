from .plaintext import PlainText
from .encrypted import Encrypted

AllTypes = [
        PlainText,
        Encrypted,
]

AllTypesDict = {}
for t in AllTypes:
    AllTypesDict[t.code] = t
