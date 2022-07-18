import sys,os,unittest
from unittest import  TestCase

from src.business.access_data_base import conectar, fecha_conexao
from src.exception.duplicated_cpf_error import DuplicatedCPF
from src.exception.field_error import EmptyFieldError, InvalidFieldError
from src.exception.cliente_not_found import ClienteNotFoundError
from src.exception.base_cliente_error import EmptyDataBaseError
from src.business.cadastro_cliente import CadastroCliente
from src.entities.cliente import Cliente

class TestCadastroCliente(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        '''Esvazia o Banco de dados e inicia o cadastro'''
        cnx = conectar()

        cursor = cnx.cursor()

        query = (
            '''SELECT  CPF FROM xpto_alimentos.cliente ''')

        cursor.execute(query)

        cpf_list = list(map(lambda x: x[0], cursor.fetchall()))

        for cpf in cpf_list:
            cls.cadastro.excluir(cpf)
        fecha_conexao(cnx, cursor)

        cls.cadastro = CadastroCliente()

        print('run SetUpclass')

    @classmethod
    def tearDown(cls) -> None:
        '''Esvazia o Banco de dados'''
        cnx = conectar()

        cursor = cnx.cursor()
        query = (
            '''SELECT  CPF FROM xpto_alimentos.cliente ''')

        cursor.execute(query)

        cpf_list = list(map(lambda x: x[0], cursor.fetchall()))

        for cpf in cpf_list:
            cls.cadastro.excluir(cpf)
        fecha_conexao(cnx, cursor)

    def test_cadastro_consultar(self):
        cliente1 = Cliente(
            'Larissa Chagas Cordeiro', '65065408573', '23412421', 'Rua A, n° 1', 'lari@email.com', '79998296149')
        cliente2 = Cliente(
            'Ingrid Barbosa', '04158952641', '324517859', 'Rua B, n° 2', 'ingrid@email.com', "79998526475")

        self.cadastro.inserir(cliente1)
        self.cadastro.inserir(cliente2)

        resultado = self.cadastro.consultar("11111111100")

        self.assertEqual("11111111100", resultado.CPF)

    def test_cadastro_inserir(self):
        cliente = Cliente(
            'Larissa Chagas Cordeiro', '65065408573', '23412421', 'Rua A, n° 1', 'lari@email.com', '79998296149')
        self.cadastro.inserir(cliente)
        resultado = self.cadastro.consultar(cliente.CPF)

        self.assertEqual("11111111100", resultado.CPF)

    def test_cadastro_listar_clientes(self):
        cliente1 = Cliente(
            'Larissa Chagas Cordeiro', '65065408573', '23412421', 'Rua A, n° 1', 'lari@email.com', '79998296149')
        cliente2 = Cliente(
            'Ingrid Barbosa', '04158952641', '324517859', 'Rua B, n° 2', 'ingrid@email.com', "79998526475")

        self.cadastro.inserir(cliente1)
        self.cadastro.inserir(cliente2)
        resultado=self.cadastro.listar_clientes()
        
        self.assertEqual(('Larissa Chagas Cordeiro','Ingrid Barbosa'),(resultado[0].nome,resultado[1].nome))

    def test_cadastro_consultar_error(self):
        with self.assertRaises(ClienteNotFoundError):
            self.cadastro.consultar("11111111100")

    def test_cadastro_excluir(self):
        cliente = Cliente(
            'Larissa Chagas Cordeiro', '65065408573', '23412421', 'Rua A, n° 1', 'lari@email.com', '79998296149')
        self.cadastro.inserir(cliente)
        self.cadastro.excluir(cliente.CPF)

        with self.assertRaises(ClienteNotFoundError):
            self.cadastro.consultar("11111111100")

    def test_cadastro_listar_clientes_error(self):
        with self.assertRaises(EmptyDataBaseError):
            self.cadastro.listar_clientes()

    def test_cadastro_excluir_error(self):
        with self.assertRaises(ClienteNotFoundError):
            self.cadastro.excluir("11111111100")

    def test_cadastro_inserir_id_error(self):
        cliente1 = Cliente(
            'Larissa Chagas Cordeiro', '65065408573', '23412421', 'Rua A, n° 1', 'lari@email.com', '79998296149')
        with self.assertRaises(InvalidFieldError):
            self.cadastro.inserir(cliente1)

    def test_cadastro_inserir_duplicatedcpf_error(self):
        cliente1 = Cliente('Larissa Chagas Cordeiro', '65065408573', '23412421', 'Rua A, n° 1', 'lari@email.com', '79998296149')
        cliente2 = Cliente('Ingrid Barbosa', '04158952641', '324517859', 'Rua B, n° 2', 'ingrid@email.com', "79998526475")
        self.cadastro.inserir(cliente2)

        with self.assertRaises(DuplicatedCPF):
            self.cadastro.inserir(cliente2)

    def test_cadastro_inserir_emptyfield_error(self):
        cliente1 = Cliente('Larissa Chagas Cordeiro', '65065408573', '23412421', 'Rua A, n° 1', 'lari@email.com', '79998296149')
        with self.assertRaises(EmptyFieldError):
            self.cadastro.inserir(cliente1)

    def test_cadastro_inserir_invalidfield_error(self):
        cliente1 = Cliente('Larissa Chagas Cordeiro', '65065408573', '23412421', 'Rua A, n° 1', 'lari@email.com', '79998296149')
        with self.assertRaises(InvalidFieldError):
            self.cadastro.inserir(cliente1)

if __name__ == '__main__':
    unittest.main() 