from mysql.connector import connect
import pandas
from tabulate import tabulate


from src.exception.base_cliente_error import EmptyDataBaseError
from src.exception.field_error import EmptyFieldError, InvalidFieldError
from src.exception.duplicated_cpf_error import DuplicatedCPF
from src.business.access_data_base import conectar, fecha_conexao
from src.entities.conta import Conta

from src.exception.conta_not_found import ContaNotFoundError
from mysql.connector.errors import IntegrityError,DatabaseError

class CadastroConta():

    def __init__(self):
        self.__campos: list = ['numero_da_conta', 'senha', 'saldo']

    def inserir(self, conta: Conta):
        cnx = conectar()

        cursor = cnx.cursor()

        adiciona_conta = (
            """INSERT INTO conta
            (numero_da_conta, senha, saldo) 
            VALUES ( %(numero_da_conta)s, %(senha)s, %(saldo)s)"""
        )

        dados = {
            "numero_da_conta": conta.numero_da_conta,
            "senha": conta.senha,
            "saldo": conta.saldo
        }

        campos_info=[i for i in dados.values()]

        try:
            cursor.execute(adiciona_conta, dados)

            conta_list = list(map(lambda x: x[0], cursor.fetchall()))

            cursor.close()

            cursor = cnx.cursor()

        except IntegrityError:
            if str(conta.numero_da_conta) not in [conta_list]:
                raise InvalidFieldError("Numero da conta invalido.")
            else:
                raise DuplicatedCPF("CPF já cadastrado")
                
        except DatabaseError:
            if '' in campos_info or None in campos_info:
                raise EmptyFieldError('Campo da conta nao pode ser nulo ou vazio')
            else:
                raise InvalidFieldError('Dado de conta invalido')

        fecha_conexao(cnx,cursor)

    def consultar(self, cpf: str) -> Conta:

        cnx = conectar()

        cursor = cnx.cursor()

        query = (
            '''SELECT CPF FROM xpto_cliente.conta''')

        cursor.execute(query)

        cpf_list = list(map(lambda x: x[0], cursor.fetchall()))

        cursor.close()
        
        cursor = cnx.cursor()

        if cpf in cpf_list:
            query = ('''SELECT numero_da_conta, senha, saldo
            FROM conta WHERE CPF=%s''')
            cursor.execute(query, [cpf])
            for (numero_da_conta, senha, saldo) in cursor:
                conta = Conta(
                    numero_da_conta, senha, saldo)
        else:
            cursor.close()
            cnx.close()
            raise ContaNotFoundError("Conta não encontrada.")

        fecha_conexao(cnx,cursor)

        return conta

    def excluir(self, cpf: str) -> None:

        cnx = conectar()

        cursor = cnx.cursor()

        deleta_conta = (
            '''DELETE FROM conta 
        WHERE CPF = %s'''
        )
        cursor.execute('''SELECT CPF 
        FROM xpto_cliente.conta''')
        cpf_list = list(map(lambda x: x[0], cursor.fetchall()))
        
        if cpf in cpf_list:
            cursor.execute(deleta_conta, (cpf,))    
        else:
            cursor.close()
            cnx.close()
            raise ContaNotFoundError("Conta não encontrada.")

        fecha_conexao(cnx,cursor)

    def alterar_cadastro(self, cpf: str) -> None:

        cnx = conectar()

        cursor = cnx.cursor()

        # Listagem de cpf no database
        cursor.execute('''SELECT CPF 
        FROM xpto_cliente.conta''')
        cpf_list = list(map(lambda x: x[0], cursor.fetchall()))

        if cpf in cpf_list:
            for i in range(len(self.__campos)):
                print(f"{i}----{self.__campos[i]}")

            index = int(input('Informe o codigo do campo a ser alterado:'))

            if index not in range(len(self.__campos)):
                print('codigo de campo nao existe')
            else:
                alteraçao = input('Nova info:\n')

            if alteraçao == None or alteraçao.isspace() or alteraçao == '':
                print('novo dado nao pode ser vazio')
            else:
                if "s" == input(f'Deseja alterar {self.__campos[index]} para "{alteraçao}"?(s/n) '):
                    sql = "UPDATE conta SET " + \
                        self.__campos[index]+" = %s WHERE CPF = %s"
                    cursor.execute(sql, (alteraçao, cpf))
                    cnx.commit()
                    print("alteracao feita")
        else:
            raise ContaNotFoundError("Conta não encontrada.")


        fecha_conexao(cnx,cursor)

    def listar_contas(self) -> list:

        cnx = conectar()
        
        cursor = cnx.cursor()

        lista_contas = (
            '''SELECT CPF 
        FROM xpto_cliente.conta'''
        )
        cursor.execute(lista_contas)
        cpf_list = list(map(lambda x: x[0], cursor.fetchall()))

        if cpf_list== []:
            cursor.close()
            cnx.close()
            raise EmptyDataBaseError("Nao tem contas cadastradas.")

        else:
            contas_list=[]
            for cpf in cpf_list:
                conta=self.consultar(cpf)

                contas_list.append(conta)

            conta_data={
                    'numero_da_conta':[f.numero_da_conta for f in contas_list],
                    'senha':[f.senha for f in contas_list],
                    'saldo':[f.saldo for f in contas_list]
                        }

            df=pandas.DataFrame(conta_data)

            print(tabulate(df, headers='keys', tablefmt='psql'))

    
        fecha_conexao(cnx,cursor)

        return contas_list