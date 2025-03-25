from django.db import models
from django.db.models import Max
from .items_model import Items

# Purchase model
class Purchases(models.Model):
    code = models.CharField(max_length=10, unique=True, db_index=True)
    date = models.DateField()
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.code
    
    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()

    def save(self, *args, **kwargs):
        if not self.code: 
            last_code = Purchases.objects.aggregate(last=Max('code'))['last']
            if last_code:
                last_number = int(last_code.split('-')[1]) 
                next_number = last_number + 1
            else:
                next_number = 1

            self.code = f"P-{next_number:03d}"
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Purchase"
        verbose_name_plural = "Purchases"
        ordering = ['date']

class PurchaseDetails(models.Model):
    item_code = models.ForeignKey(Items, to_field='code', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.IntegerField()
    header_code = models.ForeignKey(Purchases, to_field='code', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.item_code.name
    
    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            item = Items.objects.get(code=self.item_code.code)
            item.stock += self.quantity
            item.balance += self.quantity * self.unit_price
            
            item.save()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Purchase Detail"
        verbose_name_plural = "Purchase Details"
        ordering = ['item_code']
