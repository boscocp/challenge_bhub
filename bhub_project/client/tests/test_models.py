from django.test import TestCase
from mongoengine import connect, disconnect
from client.models import Cliente, DadosBancarios
from bson.decimal128 import Decimal128
from django.core.exceptions import ObjectDoesNotExist


class ModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        connect('bhub_project_test', host='mongomock://localhost')

    @classmethod
    def tearDownClass(cls):
        disconnect()

    def test_dados_cliente_salvo_deve_retornar_ok(self):
        Cliente.objects.create(
            razao_social='CNPJ',
            telefone='112222-222',
            endereco='Ali na rua',
            faturamento_declarado=100.51,
        )

        cliente = Cliente.objects.first()
        field_label = cliente._meta.get_field('razao_social').verbose_name
        self.assertEquals(field_label, 'razao social')
        self.assertEquals(cliente.razao_social, 'CNPJ')
        self.assertEquals(cliente.telefone, '112222-222')
        self.assertEquals(cliente.endereco, 'Ali na rua')
        self.assertEquals(cliente.faturamento_declarado, Decimal128('100.51'))

    def test_update_client_deve_retornar_dados_atualizados(self):
        Cliente.objects.create(
            razao_social='CNPJ',
            telefone='112222-222',
            endereco='Ali na rua',
            faturamento_declarado=100.51,
        )

        cliente = Cliente.objects.first()
        cliente.endereco = "Rua Ytaipu"
        cliente.faturamento_declarado = 555.55
        cliente.save()
        updated_cliente = Cliente.objects.first()
        self.assertEquals(updated_cliente.endereco, 'Rua Ytaipu')
        self.assertEquals(
            updated_cliente.faturamento_declarado, Decimal128('555.55'))
        self.assertEquals(updated_cliente.telefone, cliente.telefone)

    def test_delete_client_deve_retornar_ObjectDoesNotExist(self):
        Cliente.objects.create(
            uuid=1,
            razao_social='CNPJ',
            telefone='112222-222',
            endereco='Ali na rua',
            faturamento_declarado=100.51,
        )

        Cliente.objects.first().delete()
        with self.assertRaises(ObjectDoesNotExist, msg='Cliente matching query does not exist'):
            Cliente.objects.get(uuid=1)

    def test_adiciona_banco_sdeve_retornar_dois_bancos(self):
        cliente = Cliente(
            razao_social='CPF',
            telefone='112222-222',
            endereco='Ali na rua',
            faturamento_declarado=100.51,
        )
        cliente.save()
        banco_a = DadosBancarios(
            agencia=1,
            conta=2,
            banco="banco1",
            cliente=cliente,
        )
        banco_a.save()

        cliente = Cliente.objects.first()
        banco_b = DadosBancarios(
            uuid=2,
            agencia=1,
            conta=2,
            banco="banco2",
            cliente=cliente,
        )
        banco_b.save()
        bancos = DadosBancarios.objects.all()

        self.assertEquals(len(bancos), 2)

    def test_deleta_cliente_cascata_deve_retornar_ObjectDoesNotExist(self):
        cliente = Cliente(
            uuid=2,
            razao_social='CPF',
            telefone='112222-222',
            endereco='Ali na rua',
            faturamento_declarado=100.51,
        )
        cliente.save()
        novo_banco = DadosBancarios(
            uuid=1,
            agencia=1,
            conta=2,
            banco="banco1",
            cliente=cliente,
        )
        novo_banco.save()

        Cliente.objects.get(uuid=2).delete()
        with self.assertRaises(ObjectDoesNotExist, msg='DadosBancarios matching query does not exist'):
            DadosBancarios.objects.get(uuid=1)
        with self.assertRaises(ObjectDoesNotExist, msg='DadosBancarios matching query does not exist'):
            DadosBancarios.objects.get(uuid=2)
