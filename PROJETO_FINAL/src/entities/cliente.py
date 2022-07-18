from src.entities.conta import Conta
from src.business.access_data_base import conectar, fecha_conexao

class Cliente():
    def __init__(self, conta: str, nome: str, CPF: str, RG: str, endereço: str, profissao: str, email: str, telefone: str) -> None:
        self.__conta: str = conta
        self.__nome: str = nome
        self.__CPF: str = CPF
        self.__RG: str = RG
        self.__endereço: str = endereço
        self.__profissao: str = profissao
        self.__email: str = email
        self.__telefone: str = telefone

    @property
    def conta(self) -> str:
        return self.__conta

    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def CPF(self) -> str:
        return self.__CPF

    @property
    def RG(self) -> str:
        return self.__RG

    @property
    def endereço(self) -> str:
        return self.__endereço

    @property
    def profissao(self) -> str:
        return self.__profissao
        
    @property
    def email(self) -> str:
        return self.__email

    @property
    def telefone(self) -> str:
        return self.__telefone

    def conta(self) -> Conta:
        '''
        Retorna a classe conta associada ao cliente
        '''
        cnx = conectar()

        cursor = cnx.cursor()

        query = (
            '''SELECT numero_da_conta, senha, saldo 
        FROM conta 
        WHERE numero_da_conta=%s'''
        )

        cursor.execute(query, [self.conta])
        for (numero_da_conta, senha, saldo) in cursor:
            conta = Conta(numero_da_conta, senha, saldo)

        fecha_conexao(cnx,cursor)
        return conta