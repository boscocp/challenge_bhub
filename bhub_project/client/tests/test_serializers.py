from django.test import TestCase
from client.serializers import validar_banco
from django.core.exceptions import ValidationError


class SerializersTest(TestCase):
    def test_validar_conta_deve_retornar_true(self):
        self.assertTrue(validar_banco('banco1'))

    def test_validar_conta_deve_retornar_ValidationError(self):
        self.assertRaises(ValidationError, validar_banco, 'banco1#$')
