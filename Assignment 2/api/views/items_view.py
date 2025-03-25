from rest_framework import generics
from rest_framework.response import Response

from ..models.items_model import Items
from ..serializers.items_serializer import ItemsSerializer

class ItemsList(generics.ListCreateAPIView):
    queryset = Items.objects.filter(is_deleted=False)
    serializer_class = ItemsSerializer

class ItemsDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ItemsSerializer
    lookup_field = 'code'

    def get(self, request, code):
        item = Items.objects.filter(code=code, is_deleted=False).first()
        if not item:
            return Response({"message": "Item not found"}, status=404)
        
        serializer = ItemsSerializer(item)
        return Response(serializer.data)

    
    def put(self, request, code):
        item = Items.objects.filter(code=code, is_deleted=False).first()
        if not item:
            return Response({"message": "Item not found"}, status=404)
        
        serializer = ItemsSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=400)
    
    def patch(self, request, code):
        return Response({"message": "PATCH method not allowed"}, status=405)

    def delete(self, request, code):
        item = Items.objects.filter(code=code, is_deleted=False).first()
        if not item:
            return Response({"message": "Item not found"}, status=404)
        
        item.soft_delete()
        return Response({"message": "Item deleted"}, status=204)