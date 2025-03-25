from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response

from ..models.purchases_model import Purchases
from ..serializers import PurchasesSerializer, PurchaseDetailsListSerializer, PurchaseDetailsSerializer

class PurchasesList(generics.ListCreateAPIView):
    queryset = Purchases.objects.filter(is_deleted=False)
    serializer_class = PurchasesSerializer

class Purchase(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PurchasesSerializer
    lookup_field = 'code'

    def get(self, request, *args, **kwargs):
        purchase = Purchases.objects.filter(code=kwargs['code'], is_deleted=False).first()
        if not purchase:
            return Response({"message": "Item not found"}, status=404)
        
        serializer = PurchasesSerializer(purchase)
        return Response(serializer.data)
    
    def put(self, request, *args, **kwargs):
        purchase = Purchases.objects.filter(code=kwargs['code'], is_deleted=False).first()
        if not purchase:
            return Response({"message": "Item not found"}, status=404)
        
        serializer = PurchasesSerializer(purchase, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=400)
    
    def patch(self, request, *args, **kwargs):
        return Response({"message": "PATCH method not allowed"}, status=405)
    
    def delete(self, request, *args, **kwargs):
        purchase = Purchases.objects.filter(code=kwargs['code'], is_deleted=False).first()
        if not purchase:
            return Response({"message": "Item not found"}, status=404)
        
        purchase.soft_delete()
        return Response({"message": "Item deleted"}, status=204)
    

class PurchaseDetails(generics.CreateAPIView):
    serializer_class = PurchaseDetailsSerializer
    queryset = Purchases.objects.filter(is_deleted=False)

    def get(self, request, *args, **kwargs):
        try:
            purchase = Purchases.objects.prefetch_related('purchasedetails_set').get(code=kwargs['header_code'], is_deleted=False)
        except Purchases.DoesNotExist:
            return Response({"message": "Purchase not found"}, status=404)

        # Serialize the purchase along with its details
        serializer = PurchaseDetailsListSerializer(purchase)
        return Response(serializer.data)
      
    def post(self, request, *args, **kwargs):
        purchase = Purchases.objects.filter(code=kwargs['header_code'], is_deleted=False).first()
        if not purchase:
            return Response({"message": "Item not found"}, status=404)
        
        serializer = PurchaseDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(header_code=purchase)
            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)