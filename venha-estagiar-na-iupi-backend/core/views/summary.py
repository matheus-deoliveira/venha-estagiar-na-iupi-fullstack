from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from core.models import Transaction

class TransactionSummaryView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # A parte de "or 0" é para caso não tenha nada, ao invés de dar erro ele mostra 0 como resultado
        income = Transaction.objects.filter(user=request.user,type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        expense = Transaction.objects.filter(user=request.user,type='expense').aggregate(Sum('amount'))['amount__sum'] or 0

        return Response({
            "total_income": income,
            "total_expense": expense,
            "net_balance": income - expense
        })