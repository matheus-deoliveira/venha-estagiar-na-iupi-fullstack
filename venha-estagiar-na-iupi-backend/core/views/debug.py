# core/views/debug.py
import random
from datetime import date, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import Transaction

class PopulateDBView(APIView):
    """
    View utilitária para preencher o banco de dados com dados de teste.
    Gera 20 entradas e 20 saídas aleatórias.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        incomes = []
        expenses = []

        # O usuário que enviou a requisição (extraído do Token)
        current_user = request.user

        # Descrições para sortear
        desc_income = ['Salário', 'Freelance', 'Venda de Item', 'Reembolso', 'Presente', 'Dividendo']
        desc_expense = ['Mercado', 'Aluguel', 'Uber', 'Ifood', 'Cinema', 'Farmácia', 'Assinatura']

        # Criar 20 Entradas
        for _ in range(20):
            # Gera data aleatória nos últimos 60 dias
            random_days = random.randint(0, 60)
            transaction_date = date.today() - timedelta(days=random_days)
            
            t = Transaction(
                description=f"{random.choice(desc_income)} (Teste)",
                amount=random.randint(100, 5000),
                type='income',
                date=transaction_date,
                user=current_user,
            )
            incomes.append(t)

        # Criar 20 Saídas
        for _ in range(20):
            random_days = random.randint(0, 60)
            transaction_date = date.today() - timedelta(days=random_days)
            
            t = Transaction(
                description=f"{random.choice(desc_expense)} (Teste)",
                amount=random.randint(10, 500), # Saídas menores
                type='expense',
                date=transaction_date,
                user=current_user,
            )
            expenses.append(t)

        # bulk_create insere tudo de uma vez (muito mais rápido que loop save())
        Transaction.objects.bulk_create(incomes + expenses)

        return Response(
            {"message": "Sucesso! 40 transações foram criadas no banco."},
            status=status.HTTP_201_CREATED
        )