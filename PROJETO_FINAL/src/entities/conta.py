class Conta():
    def __init__(self, numero_da_conta: str, senha: str, saldo: float):
        self.__numero_da_conta = numero_da_conta
        self.__senha = senha
        self.__saldo = saldo
        
    @property
    def numero_da_conta(self) -> str:
        return self.__numero_da_conta
    
    @property
    def senha(self) -> str:
        return self.__senha    
    
    @property
    def saldo(self) -> float:
        return self.__saldo