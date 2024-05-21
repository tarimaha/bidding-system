from django.urls import path
from . import views
from django.urls import reverse


#from django.contrib.auth.views import LogoutView
 


app_name = "bids"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    #path("register", views.register, name="register"),
    path("listing/<int:listing>", views.listing, name="listing"),
    path("bid", views.bid, name="bid"),
    path("comment", views.comment, name="comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("addtowatchlist/<int:item_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path('remove_from_watchlist/<int:item_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path("categories", views.categories, name="categories"),
    path("success", views.success, name="success"),
    path("addListing", views.addListing, name="add_listing"),
    path("user_listings", views.user_listings, name="user_listings"),
    path("close_listing/<int:listing_id>", views.close_listing, name="close_listing"),
    #path('upload-profile-picture/', views.upload_profile_picture, name='upload_profile_picture'),
    path('profile/', views.profile_view, name='profile_view'),
    #path('create-profile/', views.create_profile, name='create_profile'),
    path('rate-seller/<str:seller_username>/<int:rating>/', views.rate_seller, name='rate_seller'),
    path('profile/create/', views.create_profile, name='create_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile')
]  
