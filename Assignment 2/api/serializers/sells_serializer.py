from rest_framework import serializers
from ..models.sells_model import Sells, SellDetails

class SellsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sells
        fields = ["code", "date", "description"]
        read_only_fields = ["code"]
      
class SellDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellDetails
        fields = ["item_code", "quantity", "header_code"]
        read_only_fields = ["header_code"]

class SellDetailsListSerializer(serializers.ModelSerializer):
    details = SellDetailsSerializer(source="selldetails_set", many=True, read_only=True)
    class Meta:
        model = Sells
        fields = ["code", "date", "description", "details"]
        read_only_fields = ["code"]