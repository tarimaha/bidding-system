from django.forms import ModelForm
from .models import Listing, UserProfile

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['name', 'initial', 'image', 'category']


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['address', 'phone_number', 'payment_method', 'payment_card_number', 'payment_expiry_date']

class ProfilePictureForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']
