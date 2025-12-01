from django.test import TestCase
from core.models import Transaction

class TransactionModelTest(TestCase):
    def setUp(self):
        """
        O método setUp roda antes de cada teste.
        Usamos para preparar o terreno (criar dados falsos).
        """
        self.transaction = Transaction.objects.create(
            description="Teste Unitário",
            amount=100.50,
            type="income",
            date="2023-01-01"
        )

    def test_transaction_creation(self):
        """Verifica se o objeto foi criado corretamente no banco"""
        self.assertTrue(isinstance(self.transaction, Transaction))
        self.assertEqual(self.transaction.amount, 100.50)
        self.assertEqual(str(self.transaction), "Teste Unitário (income) - R$ 100.5")