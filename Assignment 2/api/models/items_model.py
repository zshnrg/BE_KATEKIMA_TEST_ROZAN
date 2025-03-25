from django.db import models
from django.db.models import Max

# Items model
class Items(models.Model):
    code = models.CharField(max_length=10, unique=True, db_index=True)
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    stock = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

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
