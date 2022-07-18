from src.exception.not_found_error import NotFoundError

class ContaNotFoundError(NotFoundError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)