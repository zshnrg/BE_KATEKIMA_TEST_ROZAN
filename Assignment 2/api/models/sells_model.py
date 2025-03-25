from django.db import models
from django.db.models import Max, Sum
from .items_model import Items
from .purchases_model import PurchaseDetails

# Sells model
class Sells(models.Model):
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
            last_code = Sells.objects.aggregate(last=Max('code'))['last']
            if last_code:
                last_number = int(last_code.split('-')[1]) 
                next_number = last_number + 1
            else:
                next_number = 1
            
            self.code = f"S-{next_number:03d}"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Sell"
        verbose_name_plural = "Sells"
        ordering = ['date']

class SellDetails(models.Model):
    item_code = models.ForeignKey(Items, to_field='code', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    header_code = models.ForeignKey(Sells, to_field='code', on_delete=models.CASCADE)

    # Additional column for better record keeping
    unit_price = models.IntegerField(default=0)
    balance_quantity = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)

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
            purchases = list(PurchaseDetails.objects.filter(item_code=item, is_deleted=False).order_by("id"))
            total_sells = SellDetails.objects.filter(item_code=item, is_deleted=False).aggregate(total=Sum("quantity"))["total"] or 0

            sum_used_quantity = 0
            sell_quantity = 0
            sell_balance = 0
            for purchase in purchases:
                purchase_quantity = purchase.quantity

                if total_sells > sum_used_quantity:
                    used_quantity = min(purchase_quantity, total_sells - sum_used_quantity)
                    sum_used_quantity += used_quantity
                    purchase_quantity = purchase_quantity - used_quantity

                if purchase_quantity > 0:
                    quantity = min(purchase_quantity, self.quantity)
                    sell_quantity += quantity
                    sell_balance += quantity * purchase.unit_price
                    purchase_quantity = purchase_quantity - sell_quantity

                if sell_quantity == self.quantity:
                    break
            
            print(sell_quantity, self.quantity)

            if sell_quantity < self.quantity:
                raise ValueError(f"Insufficient stock for {item.name}, only {sell_quantity} available")

            item.stock -= self.quantity
            item.balance -= sell_balance

            self.unit_price = sell_balance // self.quantity
            self.balance_quantity = item.stock
            self.balance = item.balance

            item.save()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Sell Item"
        verbose_name_plural = "Sell Items"
        ordering = ['item_code']