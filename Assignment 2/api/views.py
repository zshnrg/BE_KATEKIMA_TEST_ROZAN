from django.shortcuts import render
from rest_framework import generics

from .models import Items
from .serializers import ItemsSerializer

class ItemsList(generics.ListCreateAPIView):
    queryset = Items.objects.all()
    serializer_class = ItemsSerializer

class ItemsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Items.objects.all()
    serializer_class = ItemsSerializer
    lookup_field = 'code'