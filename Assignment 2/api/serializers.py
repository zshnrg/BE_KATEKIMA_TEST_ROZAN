from rest_framework import serializers
from .models.items_model import Items

class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = ["code", "name", "unit", "description", "stock", "balance"]
        read_only_fields = ["code", "stock", "balance"]
