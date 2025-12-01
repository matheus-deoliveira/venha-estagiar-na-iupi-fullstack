from rest_framework import serializers

from core.models.transaction import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    
    class Meta:

        # Modelo desse serializer
        model = Transaction

        # Campos que serão expostos no JSON
        fields = ['id', 'description', 'amount', 'type', 'date']

    # Validação do amount
    # Pelo que estive estudando somente ter um "validate_nomedavariável"
    # já é suficiente para o django entender que é uma validação do campo
    def validate_amount(self, value):
            if value <= 0:
                raise serializers.ValidationError("O valor da transação deve ser positivo")
            return value