from django.db import models
from multiselectfield import MultiSelectField
import uuid
# Create your models here.

class Features(models.TextChoices):
    CCTV = "CCTV CAMERA", "Cctv Camera"
    FAMILY_LOUNGE = "FAMILY LOUNGE", "Family Lounge"
    SWIMMING_POOL = "SWIMMING POOL", "Swimming Pool"
    FULLY_FITTED_KITCHEN = "FULLY FITTED KITCHEN", "Fully Fitted Kitchen"
    POWER_SUPPLY = "24/7 POWER SUPPLY", "24/7 Power Supply"
    BALCONY_VIEWS = "BALCONY VIEWS", "Balcony Views"
    
class PaymentPlan(models.TextChoices):
    _3months = "3 MONTHS", "3 Months"
    _6months = "6 MONTHS", "6 Months"
    _8months = "8 MONTHS", "8 Months"
    _10months = "10 MONTHS", "10 Months"
    _12months = "12 MONTHS", "12 Months"
    
class Location(models.Model):
    lid = models.IntegerField(primary_key=True)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

class Property(models.Model):
    LAND_USE_TYPES = [
        ("RESIDENTIAL", "Residential"),
        ("COMMERCIAL", "Commercial"),
        ("MIXED USE", "Mixed use"),
    ]
    
    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('SOLD', 'Sold'),
        ('PENDING', 'Pending'),
    ]
    
    propertyId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property_type = models.CharField(max_length=200)
    property_name = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    land_use = models.CharField(choices=LAND_USE_TYPES, default="RESIDENTIAL")
    land_title = models.CharField(max_length=300)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    property_size = models.IntegerField()
    features = MultiSelectField(choices=Features.choices)
    balconies = models.IntegerField()
    serviced = models.BooleanField()
    # I need to figure out the status field for now its empty
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')
    newly_built = models.BooleanField()
    furnished = models.BooleanField()
    payment_plan = MultiSelectField(choices=PaymentPlan.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Image(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    image = models.ImageField()
    upload_at = models.DateTimeField(auto_now_add=True)