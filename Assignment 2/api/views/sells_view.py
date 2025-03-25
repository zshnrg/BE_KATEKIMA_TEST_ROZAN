from rest_framework import generics
from rest_framework.response import Response

from ..models.sells_model import Sells
from ..serializers.sells_serializer import SellsSerializer, SellDetailsListSerializer, SellDetailsSerializer

class SellsList(generics.ListCreateAPIView):
    queryset = Sells.objects.filter(is_deleted=False)
    serializer_class = SellsSerializer

class Sell(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SellsSerializer
    lookup_field = 'code'

    def get(self, request, code):
        sell = Sells.objects.filter(code=code, is_deleted=False).first()
        if not sell:
            return Response({"message": "Item not found"}, status=404)
        
        serializer = SellsSerializer(sell)
        return Response(serializer.data)
    
    def put(self, request, code):
        sell = Sells.objects.filter(code=code, is_deleted=False).first()
        if not sell:
            return Response({"message": "Item not found"}, status=404)
        
        serializer = SellsSerializer(sell, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=400)
    
    def patch(self, request, code):
        return Response({"message": "PATCH method not allowed"}, status=405)
    
    def delete(self, request, code):
        sell = Sells.objects.filter(code=code, is_deleted=False).first()
        if not sell:
            return Response({"message": "Item not found"}, status=404)
        
        sell.soft_delete()
        return Response({"message": "Item deleted"}, status=204)
    
class SellDetails(generics.CreateAPIView):
    serializer_class = SellDetailsSerializer
    queryset = Sells.objects.filter(is_deleted=False)

    def get(self, request, header_code):
        try:
            sell = Sells.objects.prefetch_related('selldetails_set').get(code=header_code, is_deleted=False)
        except Sells.DoesNotExist:
            return Response({"message": "Sell not found"}, status=404)

        # Serialize the sell along with its details
        serializer = SellDetailsListSerializer(sell)
        return Response(serializer.data)
    
    def post(self, request, header_code):
        try:
            sell = Sells.objects.get(code=header_code, is_deleted=False)
        except Sells.DoesNotExist:
            return Response({"message": "Sell not found"}, status=404)
        try:
            serializer = SellDetailsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(header_code=sell)
                return Response(serializer.data, status=201)
        except ValueError as e:
            return Response({"message": str(e)}, status=400)
        
        return Response(serializer.errors, status=400)