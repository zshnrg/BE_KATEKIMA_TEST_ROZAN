from django.db import models
from django.db.models import Max

class Manager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

# Items model
class Items(models.Model):
    code = models.CharField(max_length=10, unique=True, db_index=True)
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    stock = models.IntegerField()
    balance = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    objects = Manager()
    all_objects = models.Manager()

    def __str__(self):
        return self.name
    
    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()
    
    def save(self, *args, **kwargs):
        if not self.code: 
            last_code = Items.objects.aggregate(last=Max('code'))['last']
            if last_code:
                last_number = int(last_code.split('-')[1]) 
                next_number = last_number + 1
            else:
                next_number = 1 

            self.code = f"I-{next_number:03d}" 
        super().save(*args, **kwargs)
    
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