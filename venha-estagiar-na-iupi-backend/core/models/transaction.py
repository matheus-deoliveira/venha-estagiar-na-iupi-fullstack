from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    # Definimos as opções fixas para o campo 'type'
    # O primeiro valor é o que vai no banco ('income'), o segundo é o que aparece para humanos ('Entrada')
    TYPE_CHOICES = (
        ('income', 'Entrada'),
        ('expense', 'Saída'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transaction')

    # CharField: para textos curtos
    description = models.CharField(max_length=255)

    # DecimalField: para dinheiro
    # Float perde precisão
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    # choices: Garante que a API só aceite os itens de TYPE_CHOICES
    type = models.CharField(max_length=7, choices=TYPE_CHOICES)

    # DateField: Apenas a data, sem as horas
    date = models.DateField()

    # Essa função define como o objeto aparece se dermos um print() nele
    def __str__(self):
        return f"{self.description} ({self.type}) - R$ {self.amount}"