from django.db import models
import uuid


class Cliente(models.Model):
    class RazaoSocial(models.TextChoices):
        CHOCOLATE = 'CPF', 'Pessoa fisica'
        VANILLA = 'CNPJ', 'Pessoa juridica'
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
                            help_text='Unica ID para este cliente',
                            editable=False)
    razao_social = models.CharField(
        choices=RazaoSocial.choices, max_length=4)
    telefone = models.CharField(max_length=100)
    endereco = models.CharField(max_length=100)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    faturamento_declarado = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.razao_social}, {self.telefone}'


class DadosBancarios(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
                            help_text='Unica ID para esta conta bancaria')
    agencia = models.PositiveSmallIntegerField()
    conta = models.PositiveSmallIntegerField()
    banco = models.CharField(max_length=100)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.banco}'
