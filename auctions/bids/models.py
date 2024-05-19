from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model




User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Additional profile fields
    address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    # Payment details
    payment_method = models.CharField(max_length=50, blank=True)
    payment_card_number = models.CharField(max_length=16, blank=True)
    payment_expiry_date = models.DateField(blank=True, null=True)
    # Add more payment-related fields as needed

    seller_rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)



    def __str__(self):
        return f"{self.user.username}'s Profile"

    def is_complete(self):
        return bool(self.address and self.phone_number and self.profile_picture)

class Listing(models.Model):
    CATEGORIES = [
        ('Accessories', 'Accessories'),
        ('Antiques', 'Antiques'),
        ('Clothes', 'Clothes'),
        ('Decoration', 'Decoration'),
        ('Electronics', 'Electronics'),
        ('Valuables', 'Valuables'),
        ('Valuables', 'vehicle'),
        ('Other', 'Other'),
    ]
    STATUS = [
        ('Pending', 'Pending'),
        ('Closed', 'Closed'),
    ]
    DEFAULT_USER = 1
    name = models.CharField(max_length=100, blank=False)
    initial = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE, default=DEFAULT_USER)
    image = models.ImageField(default='None/NIA.png')
    category = models.CharField(max_length=11, choices=CATEGORIES, default='Other')
    status = models.CharField(max_length=7, choices=STATUS, default='Pending')
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - starts at ${self.initial}"

    # Used to test in test.py
    def is_valid_listing(self):
        return len(self.name) > 0 and self.initial > 0

    class Meta:
        verbose_name = "Listing"
        verbose_name_plural = "Listings"
        ordering = ['-created']

# stores the bids for the Listings
class Bid(models.Model):
    user = models.ForeignKey(User, blank = False, on_delete = models.CASCADE)
    listing = models.ForeignKey(Listing, blank = False, on_delete = models.CASCADE)
    highest_bid = models.DecimalField(max_digits = 10, decimal_places = 2)
    added = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"${self.highest_bid} - {self.user} on {self.listing.name}"


# stores the comments on the Listings
class Comment(models.Model):
    user = models.ForeignKey(User, blank = False, on_delete = models.CASCADE)
    listing = models.ForeignKey(Listing, blank = False, on_delete = models.CASCADE)
    comment = models.CharField(max_length = 400, blank = False)
    added = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.comment} - by {self.user}"
