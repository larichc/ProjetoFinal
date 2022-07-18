from mysql.connector import connect
import pandas
from tabulate import tabulate


from src.exception.base_cliente_error import EmptyDataBaseError
from src.exception.field_error import EmptyFieldError, InvalidFieldError
from src.exception.duplicated_cpf_error import DuplicatedCPF
from src.business.access_data_base import conectar, fecha_conexao
from src.entities.cliente import Cliente

from src.exception.cliente_not_found import ClienteNotFoundError
from mysql.connector.errors import IntegrityError,DatabaseError

class CadastroCliente():

    def __init__(self):
        self.__campos: list = ['conta', 'nome', 'CPF', 'RG', 'endereço', 'profissao', 'email', 'telefone']

    def inserir(self, cliente: Cliente):
        cnx = conectar()

        cursor = cnx.cursor()

        adiciona_cliente = (
            """INSERT INTO cliente
            (nome,CPF,RG,endereço,profissao,email,telefone) 
            VALUES ( %(nome)s, %(CPF)s, %(RG)s, %(endereço)s, %(profissao)s, %(email)s, %(telefone)s)"""
        )

        dados = {
            "conta": cliente.conta,
            "nome": cliente.nome,
            "CPF": cliente.CPF,
            "RG": cliente.RG,
            "endereço": cliente.endereço,
            "profissao": cliente.profissao,
            "email": cliente.email,
            "telefone": cliente.telefone
        }

        campos_info=[i for i in dados.values()]


        try:
            cursor.execute(adiciona_cliente, dados)

        except IntegrityError:
            if (cliente.conta) not in [conta_list]:
                raise InvalidFieldError("Conta invalida.")
            else:
                raise DuplicatedCPF("CPF já cadastrado")
                
        except DatabaseError:
            if '' in campos_info or None in campos_info:
                raise EmptyFieldError('Campo do cliente nao pode ser nulo ou vazio')
            else:
                raise InvalidFieldError('Dado de campo invalido')

        fecha_conexao(cnx,cursor)

    def consultar(self, cpf: str) -> Cliente:

        cnx = conectar()

        cursor = cnx.cursor()
        query = (
            '''SELECT CPF FROM xpto_alimentos.cliente ''')

        cursor.execute(query)

        cpf_list = list(map(lambda x: x[0], cursor.fetchall()))
        cursor.close()
        cursor = cnx.cursor()

        if cpf in cpf_list:
            query = ('''SELECT nome,CPF,RG,endereço,profissao,email,telefone 
            FROM cliente WHERE CPF=%s''')
            cursor.execute(query, [cpf])
            for (nome, CPF, RG, endereço, profissao, email, telefone) in cursor:
                cliente = Cliente(
                    nome, CPF, RG, endereço, profissao, email, telefone)
        else:
            cursor.close()
            cnx.close()
            raise ClienteNotFoundError("CPF não encontrado.")

        fecha_conexao(cnx,cursor)

        return cliente

    def excluir(self, cpf: str) -> None:

        cnx = conectar()

        cursor = cnx.cursor()

        deleta_cliente = (
            '''DELETE FROM cliente 
        WHERE CPF = %s'''
        )
        cursor.execute('''SELECT CPF 
        FROM xpto_alimentos.cliente''')
        cpf_list = list(map(lambda x: x[0], cursor.fetchall()))
        
        if cpf in cpf_list:
            cursor.execute(deleta_cliente, (cpf,))    
        else:
            cursor.close()
            cnx.close()
            raise ClienteNotFoundError("CPF não encontrado.")

        fecha_conexao(cnx,cursor)

    def alterar_cadastro(self, cpf: str) -> None:

        cnx = conectar()

        cursor = cnx.cursor()

        # Listagem de cpf no database
        cursor.execute('''SELECT CPF 
        FROM xpto_alimentos.cliente''')
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
                    sql = "UPDATE cliente SET " + \
                        self.__campos[index]+" = %s WHERE CPF = %s"
                    cursor.execute(sql, (alteraçao, cpf))
                    cnx.commit()
                    print("alteracao feita")
        else:
            raise ClienteNotFoundError("CPF não encontrado.")

        fecha_conexao(cnx,cursor)

    def listar_clientes(self) -> list:

        cnx = conectar()
        
        cursor = cnx.cursor()

        lista_clientes = (
            '''SELECT CPF 
        FROM xpto_alimentos.cliente'''
        )
        cursor.execute(lista_clientes)
        cpf_list = list(map(lambda x: x[0], cursor.fetchall()))

        if cpf_list== []:
            cursor.close()
            cnx.close()
            raise EmptyDataBaseError("Nao tem clientes cadastrados.")

        else:
            clientes_list=[]
            for cpf in cpf_list:
                cliente=self.consultar(cpf)

                clientes_list.append(cliente)

            cliente_data={
                    'nome':[f.nome for f in clientes_list],
                    'CPF':[f.CPF for f in clientes_list],
                    'RG':[f.RG for f in clientes_list],
                    'endereço':[f.endereço for f in clientes_list],
                    'profissao':[f.profissao for f in clientes_list],
                    'email':[f.email for f in clientes_list],
                    'telefone':[f.telefone for f in clientes_list]
                        }

            df=pandas.DataFrame(cliente_data)

            print(tabulate(df, headers='keys', tablefmt='psql'))

    
        fecha_conexao(cnx,cursor)

        return clientes_list