from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()


class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Warehouses"
    
    def __str__(self):
        return self.name


class ProductStock(models.Model):
    product_id = models.IntegerField()  # ID del producto en ProjectA
    sku = models.CharField(max_length=100, unique=True, db_index=True)
    name = models.CharField(max_length=200)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stocks')
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    reserved_quantity = models.IntegerField(default=0)
    min_stock_threshold = models.IntegerField(default=10)
    max_stock_threshold = models.IntegerField(default=500)
    last_updated = models.DateTimeField(auto_now=True)
    
    @property
    def available_quantity(self):
        return self.quantity - self.reserved_quantity
    
    def __str__(self):
        return f"{self.sku} - {self.warehouse.name}: {self.available_quantity}"
    
    class Meta:
        unique_together = ['product_id', 'warehouse']
        indexes = [
            models.Index(fields=['product_id']),
            models.Index(fields=['sku']),
        ]


class StockMovement(models.Model):
    MOVEMENT_TYPES = (
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
        ('RESERVE', 'Reserve'),
        ('RELEASE', 'Release Reserve'),
        ('TRANSFER', 'Transfer'),
    )
    
    product_stock = models.ForeignKey(ProductStock, on_delete=models.CASCADE, related_name='movements')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    reference_id = models.CharField(max_length=100, blank=True)  # Order ID from ProjectA
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.movement_type} - {self.quantity} - {self.product_stock.sku}"
