from rest_framework import serializers
from client.models import Cliente, DadosBancarios
from django.core.exceptions import ValidationError
import re


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = [
            'razao_social',
            'telefone',
            'endereco',
            'data_cadastro',
            'faturamento_declarado',
            'uuid'
        ]


class DadosBancariosSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer(source="clientes", many=True, read_only=True)

    class Meta:
        model = DadosBancarios
        fields = ['agencia', 'conta', 'banco', 'cliente', 'uuid']
        extra_kwargs = {'clientes': {'required': False}}

    def validate(self, data):
        validar_banco(data['banco'])
        return data


def validar_banco(value):
    pattern = "^[A-Za-z0-9 ]*$"
    if bool(re.match(pattern, value)):
        return value
    else:
        raise ValidationError({'banco': "Banco invlálido"})
