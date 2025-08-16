from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.

class Register(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)  # hashed

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name



class Product(models.Model):
    AVAILABILITY_CHOICES = [
        ('in_stock', 'In Stock'),
        ('out_of_stock', 'Out of Stock'),
    ]

    name = models.CharField(max_length=100)
    subsentence = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    material = models.CharField(max_length=50)
    price = models.FloatField(blank=True, null=True)
    offer = models.CharField(max_length=50)
    discount = models.CharField(max_length=50, blank=True, null=True)
    dimension = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    warranty = models.CharField(max_length=350)
    weight = models.CharField(max_length=50)
    seating_capacity = models.CharField(max_length=50, blank=True, null=True)
    availability = models.CharField(
        max_length=20,
        choices=AVAILABILITY_CHOICES,
        default='in_stock'
    )
    return_policy = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = CloudinaryField('image')

    def __str__(self):
        return f"{self.product.name} Image"




class Enquiry(models.Model):
    product_name = models.CharField(max_length=200)
    product_material = models.CharField(max_length=100)
    product_offer = models.DecimalField(max_digits=10, decimal_places=2)
    product_color = models.CharField(max_length=50)
    product_quantity = models.PositiveIntegerField()
    customer_name = models.CharField(max_length=150)
    contact_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.product_name}"





class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=1000)  # Use TextField for longer messages

    def __str__(self):
        return f"{self.name} - {self.subject}"

