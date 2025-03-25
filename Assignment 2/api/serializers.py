from rest_framework import serializers
from .models.items_model import Items
from .models.purchases_model import Purchases, PurchaseDetails

class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = ["code", "name", "unit", "description", "stock", "balance"]
        read_only_fields = ["code", "stock", "balance"]

class PurchasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchases
        fields = ["code", "date", "description"]
        read_only_fields = ["code"]

class PurchaseDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseDetails
        fields = ["item_code", "quantity", "unit_price", "header_code"]
        read_only_fields = ["header_code"]

class PurchaseDetailsListSerializer(serializers.ModelSerializer):
    details = PurchaseDetailsSerializer(source="purchasedetails_set", many=True, read_only=True)
    class Meta:
        model = Purchases
        fields = ["code", "date", "description", "details"]
        read_only_fields = ["code"]