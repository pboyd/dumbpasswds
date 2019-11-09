from .plaintext import PlainText

AllTypes = [
        PlainText,
]

AllTypesDict = {}
for t in AllTypes:
    AllTypesDict[t.code] = t
