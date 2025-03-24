from django.db import models

# Items model
class Items(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    stock = models.IntegerField()
    balance = models.IntegerField()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"
        ordering = ['name']

# Purchase model
class Purchases(models.Model):
    code = models.CharField(max_length=10)
    date = models.DateField()
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.code
    
    class Meta:
        verbose_name = "Purchase"
        verbose_name_plural = "Purchases"
        ordering = ['date']

class PurchaseItems(models.Model):
    item_code = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    header_code = models.ForeignKey(Purchases, on_delete=models.CASCADE) 

    def __str__(self):
        return self.item_code.name
    
    class Meta:
        verbose_name = "Purchase Item"
        verbose_name_plural = "Purchase Items"
        ordering = ['item_code']

# Sells model
class Sells(models.Model):
    code = models.CharField(max_length=10)
    date = models.DateField()
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.code
    
    class Meta:
        verbose_name = "Sell"
        verbose_name_plural = "Sells"
        ordering = ['date']

class SellItems(models.Model):
    item_code = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    header_code = models.ForeignKey(Sells, on_delete=models.CASCADE)

    def __str__(self):
        return self.item_code.name
    
    class Meta:
        verbose_name = "Sell Item"
        verbose_name_plural = "Sell Items"
        ordering = ['item_code']