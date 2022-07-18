class InvalidFieldError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class EmptyFieldError(InvalidFieldError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)