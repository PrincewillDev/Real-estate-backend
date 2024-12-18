from django.db import models
from django.core.validators import MinValueValidator
from multiselectfield import MultiSelectField
import uuid


class Features(models.TextChoices):
    CCTV = "CCTV CAMERA", "Cctv Camera"
    FAMILY_LOUNGE = "FAMILY LOUNGE", "Family Lounge"
    SWIMMING_POOL = "SWIMMING POOL", "Swimming Pool"
    FULLY_FITTED_KITCHEN = "FULLY FITTED KITCHEN", "Fully Fitted Kitchen"
    POWER_SUPPLY = "24/7 POWER SUPPLY", "24/7 Power Supply"
    BALCONY_VIEWS = "BALCONY VIEWS", "Balcony Views"


class PaymentPlan(models.TextChoices):
    _3MONTHS = "3 MONTHS", "3 Months"
    _6MONTHS = "6 MONTHS", "6 Months"
    _8MONTHS = "8 MONTHS", "8 Months"
    _10MONTHS = "10 MONTHS", "10 Months"
    _12MONTHS = "12 MONTHS", "12 Months"


class Location(models.Model):
    id = models.AutoField(primary_key=True)  # Use AutoField for primary key
    state = models.CharField(max_length=100, null=False, blank=False)
    city = models.CharField(max_length=100, null=False, blank=False)
    address = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return f"{self.address}, {self.city}, {self.state}"


class Property(models.Model):
    LAND_USE_TYPES = [
        ("RESIDENTIAL", "Residential"),
        ("COMMERCIAL", "Commercial"),
        ("MIXED USE", "Mixed use"),
    ]
    STATUS_CHOICES = [
        ("OFFPLAN", "Offplan"),
        ("READYTOMOVEIN", "Ready to Move In"),
        ("AVAILABLE", "Available"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property_type = models.CharField(max_length=200)
    property_name = models.CharField(max_length=300)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    description = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="properties")
    land_use = models.CharField(choices=LAND_USE_TYPES, default="RESIDENTIAL", max_length=20)
    land_title = models.CharField(max_length=300)
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    property_size = models.PositiveIntegerField()
    features = MultiSelectField(choices=Features.choices, blank=True)
    balconies = models.PositiveIntegerField(default=0)
    serviced = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="AVAILABLE")
    newly_built = models.BooleanField(default=False)
    furnished = models.BooleanField(default=False)
    payment_plan = MultiSelectField(choices=PaymentPlan.choices, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.price <= 0:
            raise ValueError("Price must be a positive value.")
        if self.bedrooms < 0 or self.bathrooms < 0:
            raise ValueError("Bedrooms and Bathrooms cannot be negative.")

    def __str__(self):
        return self.property_name


class Image(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="properties/images/")
    upload_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.property}"


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    client_name = models.CharField(max_length=70, null=False, blank=False)
    message = models.TextField(max_length=300, null=False, blank=False)

    def __str__(self):
        return f"Review by {self.client_name}"


class Team(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    image = models.ImageField(upload_to="team/images/")

    def __str__(self):
        return self.name


class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    phone_number = models.JSONField()  # Ensure validation for proper formatting

    def __str__(self):
        return self.email
