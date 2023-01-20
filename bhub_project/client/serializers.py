from rest_framework import serializers
from client.models import Cliente, DadosBancarios


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = [
            'razao_social',
            'telefone',
            'endereco',
            'data_cadastro',
            'faturamento_declarado'
        ]


class DadosBancariosSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer(source="clientes", many=True, read_only=True)

    class Meta:
        model = DadosBancarios
        fields = ['agencia', 'conta', 'banco', 'cliente']
        extra_kwargs = {'clientes': {'required': False}}
