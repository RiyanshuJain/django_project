from django.db import models

# Create your models here.
class Invoice(models.Model):
    date = models.DateField(auto_now_add=True)
    invoice_number = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=100)

class InvoiceDetail(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='invoice_details', on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    
    def save(self, *args, **kwargs):
        self.price = self.quantity * self.unit_price
        super().save(*args, **kwargs)