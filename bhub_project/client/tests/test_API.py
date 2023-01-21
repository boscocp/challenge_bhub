from uuid import UUID
from django.test import TestCase
from client.models import Cliente, DadosBancarios
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.test import APIClient
from mongoengine import connect, disconnect
from bson.decimal128 import Decimal128

client = APIClient()
# Create your tests here.


class APITest(TestCase):

    @classmethod
    def setUpTestData(cls):
        connect('bhub_project_test', host='mongomock://localhost')

    @classmethod
    def tearDownClass(cls):
        disconnect()

    def test_API_post_deve_retornar_201(self):
        request = {
            "cliente": {
                "razao_social": "CPF",
                "telefone": "1155555",
                "endereco": "Rua Api",
                "faturamento_declarado": 1054.51
            }
        }
        response = client.post('/clientes/', request, format='json')
        self.assertEqual(response.status_code, 201)

    def test_API_post_deve_retornar_400(self):
        request = {
            "cliente": {
                "razao_social": None,
                "telefone": "1155555",
                "endereco": "Rua Api",
                "faturamento_declarado": 123.55
            }
        }
        response = client.post('/clientes/', request, format='json')
        self.assertEqual(response.status_code, 400)

    def test_view_get_deve_retornar_3_objetos_e_200(self):
        Cliente.objects.create(
            razao_social='CNPJ',
            telefone='112222-222',
            endereco='Ali na rua',
            faturamento_declarado=100.51,
        )
        Cliente.objects.create(
            razao_social='divorciado',
            telefone='112222-232',
            endereco='Ali na rua',
            faturamento_declarado=100.51,
        )
        Cliente.objects.create(
            razao_social='CPF',
            telefone='112222-242',
            endereco='Ali na rua',
            faturamento_declarado=100.51,
        )
        response = client.get('/clientes/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_view_get_deve_retornar_lista_vazia(self):
        response = client.get('/clientes/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_get_by_uuid_deve_retornar_200(self):
        Cliente.objects.create(
            uuid=UUID("35fc86f3-5533-412b-8ce0-93107079b469"),
            razao_social='CNPJ',
            telefone='112222-222',
            endereco='Ali na rua',
            faturamento_declarado=100.51,
        )
        response = client.get(
            '/clientes/35fc86f3-5533-412b-8ce0-93107079b469/')
        self.assertEqual(response.status_code, 200)

    def test_get_deve_retornar_404(self):
        response = client.get(
            '/clientes/35fc86f3-5533-412b-8ce0-93107079b469/')
        self.assertEqual(response.status_code, 404)

    def test_update_cliente_deve_retornar_telefone_endereco_faturamento_modificados(self):
        Cliente.objects.create(
            uuid=UUID("35fc86f3-5533-412b-8ce0-93107079b469"),
            razao_social='CNPJ',
            telefone='112222-222',
            endereco='Ali na rua',
            faturamento_declarado=100.51,
        )
        request = {
            "cliente": {
                "razao_social": "CPF",
                "telefone": "1155555",
                "endereco": "Rua Api",
                "faturamento_declarado": 1054.51
            }
        }
        response = client.put(
            '/clientes/35fc86f3-5533-412b-8ce0-93107079b469/', request, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.data['telefone'], "1155555")
        self.assertEquals(response.data['endereco'], "Rua Api")
        self.assertEquals(
            response.data['faturamento_declarado'], '1054.51')

    def test_delete_cliente_deve_retornar_204(self):
        Cliente.objects.create(
            uuid=UUID("35fc86f3-5533-412b-8ce0-93107079b469"),
            razao_social='CNPJ',
            telefone='112222-222',
            endereco='Ali na rua',
            faturamento_declarado=100.51,
        )
        response = client.delete(
            '/clientes/35fc86f3-5533-412b-8ce0-93107079b469/')
        self.assertEqual(response.status_code, 204)

    def test_create_dados_bancarios_deve_retornar_201(self):
        Cliente.objects.create(
            uuid=UUID("35fc86f3-5533-412b-8ce0-93107079b469"),
            razao_social='CNPJ',
            telefone='112222-222',
            endereco='Ali na rua',
            faturamento_declarado=100.51,
        )
        request = {
            "dadosbancarios": {
                "agencia": 1,
                "conta": 3,
                "banco": "Banco11",
            }
        }
        response = client.post(
            '/clientes/35fc86f3-5533-412b-8ce0-93107079b469/dadosbancarios/', request, format='json')
        self.assertEqual(response.status_code, 201)

    def test_get_all_dados_bancarios_deve_retornar_200_e_2_bancos(self):
        cliente = Cliente.objects.create(
            uuid=UUID("35fc86f3-5533-412b-8ce0-93107079b468"),
            razao_social='CNPJ',
            telefone='112222-222',
            endereco='Ali na rua',
            faturamento_declarado=100.51,
        )

        novo_banco = DadosBancarios(
            agencia=1,
            conta=2,
            banco="banco1",
            cliente=cliente,
        )
        novo_banco.save()
        novo_banco2 = DadosBancarios(
            agencia=1,
            conta=2,
            banco="banco2",
            cliente=cliente,
        )
        novo_banco2.save()
        response = client.get(
            '/clientes/35fc86f3-5533-412b-8ce0-93107079b468/dadosbancarios/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_get_dados_bancarios_by_id(self):
        cliente = Cliente.objects.create(
            uuid=UUID("35fc86f3-5533-412b-8ce0-93107079b469"),
            razao_social='CNPJ',
            telefone='112222-222',
            endereco='Ali na rua',
            faturamento_declarado=100.51,
        )

        novo_banco = DadosBancarios( 
            agencia = 1,
            conta = 2,
            banco = "banco1",
            cliente = cliente,
        )
        novo_banco.save()
        response = client.get('/clientes/35fc86f3-5533-412b-8ce0-93107079b469/dadosbancarios/'+novo_banco.uuid.__str__()+'/')
        self.assertEqual(response.status_code, 200)

    def test_update_dados_bancarios(self):
        cliente = Cliente.objects.create(
            uuid=UUID("35fc86f3-5533-412b-8ce0-93107079b469"),
            razao_social='CNPJ',
            telefone='112222-222',
            endereco='Ali na rua',
            faturamento_declarado=100.51,
        )
        novo_banco = DadosBancarios( 
            agencia = 1,
            conta = 2,
            banco = "banco1",
            cliente = cliente,
        )
        novo_banco.save()
        
        request = {
            "dadosbancarios": {
                "agencia": 54,
                "conta": 333,
                "banco": "Banco_update",
            }
        }
        response = client.put('/clientes/35fc86f3-5533-412b-8ce0-93107079b469/dadosbancarios/'+novo_banco.uuid.__str__()+'/', request, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.data['banco'], "Banco_update")

    def test_delete_dados_bancarios_deve_retornar_204(self):
        cliente = Cliente.objects.create(
            uuid=UUID("35fc86f3-5533-412b-8ce0-93107079b469"),
            razao_social='CNPJ',
            telefone='112222-222',
            endereco='Ali na rua',
            faturamento_declarado=100.51,
        )
        
        novo_banco = DadosBancarios( 
            agencia = 1,
            conta = 2,
            banco = "banco1",
            cliente = cliente,
        )
        novo_banco.save()
        response = client.delete('/clientes/35fc86f3-5533-412b-8ce0-93107079b469/dadosbancarios/'+novo_banco.uuid.__str__()+'/')
        self.assertEqual(response.status_code, 204)
