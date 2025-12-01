import json
from django.urls import reverse
from rest_framework import status
from django.test import TestCase
from core.models import Transaction

class TransactionAPITest(TestCase):
    
    def setUp(self):
        # Definimos as URLs usando 'reverse' para não fazer hardcode '/api/transactions/'
        # O padrão do DRF Router é 'nomedobasename-list' e 'nomedobasename-detail'
        self.list_url = reverse('transaction-list') 
        self.summary_url = reverse('summary')

        # Criamos alguns dados iniciais para testes de leitura
        self.t1 = Transaction.objects.create(description="Salário", amount=1000, type="income", date="2023-01-01")
        self.t2 = Transaction.objects.create(description="Aluguel", amount=300, type="expense", date="2023-01-05")

    def test_get_all_transactions(self):
        """Deve retornar status 200 e a lista de transações"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verifica se vieram 2 itens (ou verifica dentro de 'results' se tiver paginação)
        # Se tiver paginação, use: len(response.data['results'])
        self.assertEqual(response.data['count'], 2) 

    def test_create_transaction_success(self):
        """Deve criar uma nova transação com sucesso"""
        data = {
            "description": "Freelance",
            "amount": 500.00,
            "type": "income",
            "date": "2023-02-01"
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 3) # Eram 2, agora deve ter 3

    def test_create_transaction_negative_amount_fail(self):
        """Deve falhar (400) se tentar criar valor negativo"""
        data = {
            "description": "Erro",
            "amount": -50.00, # Valor inválido
            "type": "expense",
            "date": "2023-02-01"
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Garante que a mensagem de erro fala sobre o valor positivo
        # (Dependendo de como você escreveu o serializer, o erro pode estar em 'amount' ou 'non_field_errors')
        self.assertTrue('amount' in response.data) 

    def test_filter_by_type(self):
        """Deve filtrar apenas 'expense' quando solicitado na URL"""
        response = self.client.get(f"{self.list_url}?type=expense")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Deve vir apenas 1 (o Aluguel)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['description'], 'Aluguel')

    def test_summary_calculation(self):
        """Deve calcular corretamente o saldo final"""
        # Salário (1000) - Aluguel (300) = 700
        response = self.client.get(self.summary_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['total_income']), 1000.00)
        self.assertEqual(float(response.data['total_expense']), 300.00)
        self.assertEqual(float(response.data['net_balance']), 700.00)

    def test_update_transaction(self):
        """Deve atualizar uma transação existente (PUT)"""
        # Vamos editar a transação t1 (Salário) que criamos no setUp
        # Para rotas de detalhe (um item só), o DRF usa 'basename-detail'
        url = reverse('transaction-detail', args=[self.t1.id])
        
        data = {
            "description": "Salário Atualizado",
            "amount": 1500.00,
            "type": "income",
            "date": "2023-01-01"
        }
        
        response = self.client.put(
            url, 
            json.dumps(data), 
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Recarrega o objeto do banco para ver se mudou mesmo
        self.t1.refresh_from_db() 
        self.assertEqual(self.t1.description, "Salário Atualizado")
        self.assertEqual(float(self.t1.amount), 1500.00)

    def test_delete_transaction(self):
        """Deve deletar uma transação (DELETE)"""
        url = reverse('transaction-detail', args=[self.t1.id])
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verifica se o objeto sumiu do banco
        self.assertFalse(Transaction.objects.filter(id=self.t1.id).exists())

    def test_filter_by_description(self):
        """Deve filtrar por busca textual parcial"""
        # Busca por 'luguel' deve achar 'Aluguel'
        response = self.client.get(f"{self.list_url}?description=luguel")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['description'], 'Aluguel')