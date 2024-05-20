from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mail

from decimal import *

from django.conf import settings
from .models import User, Listing, Bid, Comment, UserProfile, WatchList
from .forms import ListingForm, ProfilePictureForm, UserProfileForm

from .decorators import Unauthenticated_user, Authenticated_user

# dictionary variable to keep track of individual's watchlist
watch_list = dict()

def index(request):
    listings = []
    items = Listing.objects.filter(status="Pending")
    for item in items:
        try:
            bid = Bid.objects.get(listing=item)
        except:
            bid = None
        listings.append({
            'listing': item,
            'bid': bid,
        })
    context = {
        'listings': listings,
    }
    return render(request, "auctions/index.html", context)

@Unauthenticated_user
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
       # username = request.POST["username"]
       # password = request.POST["password"]
       # user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("bids:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


@Authenticated_user
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("bids:index"))

@Unauthenticated_user
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("bids:index"))
    else:
        return render(request, "auctions/register.html")

@Authenticated_user
def listing(request, listing):
    item = Listing.objects.get(pk=listing)
    old_bid = Bid.objects.filter(listing=item)
    if item.status == 'Closed':
        try: # fails if no bid was placed on the item when it was closed
            bid = old_bid[0]
            if bid.user == request.user:
                context = {
                    'listing': item,
                    'bid': bid,
                }
                return render(request, 'auctions/success.html', context)
        except:
            return render(request, 'auctions/closed.html') # return after try fails
        return render(request, 'auctions/closed.html') # return after try passes and the if statement fails
    comments = Comment.objects.filter(listing=item)
    if old_bid.count() is 1:
        default_bid = old_bid[0].highest_bid + 10
    else:
        default_bid = item.initial + 10
    try:
        bid_info = Bid.objects.get(listing=item)
    except:
        bid_info = None;
    context = {
        'listing': item,
        'bid': bid_info,
        'comments': comments,
        'default_bid': default_bid,
    }
    return render(request, "auctions/listing.html", context)



@Authenticated_user
def bid(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    current_bid = float(request.POST['bid'])
    user = request.user

    # Assuming you have a form to handle the bid amount
    if current_bid > listing.initial:
        new_bid = Bid(listing=listing, user=user, highest_bid=current_bid)
        new_bid.save()

        # Notify users watching this item
        notify_watchers(listing, user)

        return redirect('listing', listing_id=listing.id)

def notify_watchers(listing, new_bidder):
    for watcher in WatchList.objects.filter(listing=listing).exclude(user=new_bidder):
        send_mail(
            'New bid on item you are watching',
            f'There is a new bid on the item {listing.title}. Check it out!',
            settings.DEFAULT_FROM_EMAIL,
            [watcher.user.email],
            fail_silently=False,
        )


@Authenticated_user
def comment(request):
    if request.method == "POST":
        content = request.POST["content"]
        item_id = request.POST["list_id"]
        item = Listing.objects.get(pk=item_id)
        newComment = Comment(user=request.user, comment=content, listing=item)
        newComment.save()
        return redirect("bids:listing", item_id)
    return redirect("bids:index")

@Authenticated_user
def watchlist(request):
    watch_list = WatchList.objects.filter(user=request.user)
    if not watch_list:
        context = {
            'message': "Nothing in your watchlist",
        }
        return render(request, "auctions/watchlist.html", context)

    listings = []
    for watch in watch_list:
        item = watch.listing
        try:
            bid = Bid.objects.get(listing=item)
        except Bid.DoesNotExist:
            bid = None
        listings.append({
            'listing': item,
            'bid': bid,
        })

    context = {
        'listings': listings,
    }
    return render(request, "auctions/watchlist.html", context)

@Authenticated_user
def add_to_watchlist(request, item_id):
    if request.user not in watch_list:
        watch_list[request.user] = []
        watch_list[request.user].append(item_id)
        messages.success(request, 'Successfully added item to your WatchList.', fail_silently=True)
    elif item_id in watch_list[request.user]:
        messages.warning(request, 'Item already present in your WatchList.', fail_silently=True)
    else:
        watch_list[request.user].append(item_id)
        messages.success(request, 'Successfully added item to your WatchList.', fail_silently=True)
    return redirect("bids:index")

@Authenticated_user
def remove_from(request, item_id):
    if request.user not in watch_list:
        messages.warning(request, 'Cannot remove from empty WatchList.', fail_silently=True)
    elif item_id in watch_list[request.user]:
        watch_list[request.user].remove(item_id)
        messages.success(request, 'Successfully removed item from your WatchList.', fail_silently=True)
    else:
        messages.warning(request, 'Item not in your WatchList.', fail_silently=True)
    return redirect("bids:index")

def categories(request):
    category = dict()
    listings = Listing.objects.filter(status="Pending")
    for item in listings:
        try:
            bid = Bid.objects.get(listing=item)
        except:
            bid = None
        if item.category not in category:
            category[item.category] = []
        category[item.category].append({
            'listing': item,
            'bid': bid,
        })
    context = {
        'category_list': category,
    }
    return render(request, "auctions/category.html", context)

@Authenticated_user
def success(request):
    return render(request, "auctions/success.html")

@Authenticated_user
def addListing(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES or None)

        if form.is_valid():
            newListing = form.save(commit=False)
            newListing.user = request.user
            newListing.save()
            messages.success(request, 'Successfully created your listing.', fail_silently=True)
        else:
            messages.error(request, 'Invalid Listing!', fail_silently=True)
            return redirect("bids:add_listing")
        return redirect("bids:index")
    form = ListingForm()
    context = {
        'form': form,
    }
    return render(request, "auctions/addListing.html", context)

@Authenticated_user
def user_listings(request):
    listings = []
    current_user_listings = Listing.objects.filter(user=request.user, status='Pending')
    for item in current_user_listings:
        try:
            bid = Bid.objects.get(listing=item)
        except:
            bid = None
        listings.append({
            'listing': item,
            'bid': bid,
        })
    context = {
        'listings': listings,
    }
    return render(request, "auctions/userlistings.html", context)

@Authenticated_user
def close_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if listing.user == request.user:
        listing.status = 'Closed'
        listing.save()
        messages.success(request, 'Listing successfully closed.', fail_silently=True)
    else:
        messages.warning(request, 'Unable to close listing! Authentication error.', fail_silently=True)

    return redirect("bids:user_listings")




@Authenticated_user
def rate_seller(request, seller_username, rating):
    if request.method == "POST":
        # Calculate new seller rating and update UserProfile
        seller_profile = UserProfile.objects.get(user__username=seller_username)
        seller_profile.seller_rating = (seller_profile.seller_rating + rating) / 2
        seller_profile.save()
        return redirect("bids:index")
    else:
        return render(request, "auctions/rate_seller.html")

@Authenticated_user
def create_profile(request):
    if request.method == "POST":
        profile_form = UserProfileForm(request.POST)
        
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user
            
            profile.save()
            return redirect('profile_view')
    else:
        profile_form = UserProfileForm()
        

    context = {
        'profile_form': profile_form,
        
    }
    return render(request, 'auctions/create_profile.html', context)




@Authenticated_user
def profile_view(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        is_complete = bool(user_profile.address and user_profile.phone_number)
        context = {
        'user_profile': user_profile,
        'is_complete': is_complete,
    }
        if not user_profile.is_complete:
            return redirect('auctions/create_profile')
        return render(request, 'auctions/profile.html', {'user_profile': user_profile})
    except UserProfile.DoesNotExist:
        return redirect('auctions/create_profile')  

    



@Authenticated_user
def edit_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return redirect('bids:create_profile')

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('bids:profile_view')
    else:
        form = UserProfileForm(instance=user_profile)

    context = {
        'form': form,
    }
    return render(request, 'auctions/edit_profile.html', context)