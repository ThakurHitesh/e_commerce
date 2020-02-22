from rest_framework import serializers
from api.models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

    def create(self, validated_data):
        payment = Payment.create_payment(cart_order=validated_data['cart_order'],
                                            amount=validated_data['amount'],
                                            currency=validated_data['currency'] if validated_data.get('currency') else 'INR',
                                            status=validated_data['status'] if validated_data.get('status') else 'created'
                    )
        return payment