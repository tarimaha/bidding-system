from django.contrib import admin

from .models import Listing, Bid, Comment, User, UserProfile, WatchList

# Register your models here.


admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(UserProfile)
admin.site.register(WatchList)

