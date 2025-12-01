from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.serializers import TransactionSerializer
from core.models.transaction import Transaction

class TransactionViewSet(viewsets.ModelViewSet):
    """
    O ViewSet seria responsável pelo CRUD, ao invés
    de termos que escrever 5 funções diferentes na mão,
    ViewSet permite a manipulação de todas essas funções
    GET, POST, PUT, PATCH, DELETE
    """

    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    # Pesquisando é completamente normal esse erro, então
    # somente ignora ele e segue o desenvolvimento
    def get_queryset(self): #type: ignore
        """
        Sobrescreve a busca padrão permitindo filtros via URL.
        Ex: /transactions/?type=income&description=salario
        """

        # Pega todas as transações
        queryset = Transaction.objects.filter(user=self.request.user).order_by('-date')

        # Preciso pegar os parâmetros que vieram na URL
        params = getattr(self.request, 'query_params', self.request.GET)
        description = params.get('description')
        transaction_type = params.get('type')

        if description:
            # 'description__icontains' faz o SQL: LIKE '%valor%'
            queryset = queryset.filter(description__icontains=description)

        if transaction_type:
            queryset = queryset.filter(type=transaction_type)

        return queryset
    
    # Quando criar, injeta o usuário logado automaticamente
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)