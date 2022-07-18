class DataBaseError(Exception):
    def __init__(self, *args: object) -> None:
        self.mensagem = args[0]
        super().__init__(*args)

class EmptyDataBaseError(DataBaseError):
    def __init__(self, *args: object) -> None:
        self.mensagem = args[0]
        super().__init__(*args)