class NoPrivateKeyError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)



class DecryptionError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)