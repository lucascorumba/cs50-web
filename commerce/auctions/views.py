from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect

from django import forms
from django.template.defaulttags import register

from .models import User, Listing, Bid, Comment, Wish
from .utils import highBid


# Choices for the dropdown menu at listing creation
CATEGORY_CHOICES = [
    ('None', 'Select a category'),
    ('Fashion', 'Fashion'),
    ('Eletronics & DIY', 'Eletronics & DIY'),
    ('Personal Care', 'Personal Care'),
    ('Furniture & Appliances', 'Furniture & Appliances')
]

# Form for listing creation
class ListingForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Title', 'class':'form-control form-title', 'required': True}))
    startingBid = forms.DecimalField(label="", widget=forms.NumberInput(attrs={'placeholder': 'Starting Bid', 'class':'form-control form-bid', 'required': True}))
    description = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'Description', 'class':'form-control textarea', 'required': True}))
    image = forms.URLField(label="", widget=forms.URLInput(attrs={'placeholder': 'Image Path', 'class':'form-control form-image', 'required': False}))
    category = forms.CharField(label="", widget=forms.Select(choices=CATEGORY_CHOICES, attrs={'class':'form-select'}))

# Form for new bids
class newBid(forms.Form):
    newBid = forms.DecimalField(label="Your Bid:", widget=forms.NumberInput(attrs={'placeholder': '$'}))

# Form for new comments
class newComment(forms.Form):
    newComment = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Comment', 'required': False}))

# Display all listings
def index(request):
    listings = Listing.objects.filter(state=True)
    bids = Bid.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings,
        "highestBids": highBid(bids),
        "title": "Active Listings"
    })

# Display closed listings
def closedIndex(request):
    listings = Listing.objects.filter(state=False)
    bids = Bid.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings,
        "highestBids": highBid(bids),
        "title": "Closed Listings"
    })

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def registerUser(request):
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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

# Register new listing
def newListing(request):
    if request.method == "POST":
        # Get data from newListing
        form = ListingForm(request.POST)
        user = User.objects.get(id=request.user.id)
        if form.is_valid():
            # Save New Listing
            f = Listing(owner = user, title = form.cleaned_data["title"], startingBid = float(form.cleaned_data["startingBid"]), 
            description = form.cleaned_data["description"], image = form.cleaned_data["image"], 
            creationTime = datetime.now(), category = form.cleaned_data["category"])
            # Start bid (enable 'highBid' to detect the auction)
            g = Bid(user = user, product = f, bid = 0)
            f.save()
            g.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/newListing.html", {
            "form": ListingForm()
        })

# Show specific listing page
def listing(request, listing):    
    listings = Listing.objects.get(pk=listing)
    bids = Bid.objects.all()
    comments = Comment.objects.filter(product=listings.id)
    try:
        user = User.objects.get(pk=request.user.id)              
        # Check if product is in user's watchlist
        watch = Wish.objects.filter(user=user, wishlist=listings)
        if watch:
            watchStatus = True
        else:
            watchStatus = False
        # Check if user is the owner of the listing
        if listings.owner == user:
            isOwner = True
        else:
            isOwner = False
        # Check if user is the current winner of the auction
        auctionBids = Bid.objects.filter(product=listings)
        bestBid = 0
        winner = 0
        for bid in auctionBids:
            if bid.bid > bestBid:
                winner = bid.user
            else:
                continue
        return render(request, "auctions/listing.html", {
            "listing": listings,
            "bids": highBid(bids),
            "comments": comments,
            "bidForm": newBid(),
            "commentForm": newComment(),
            "isInWatch": watchStatus,
            "isOwner": isOwner,
            "isActive": listings.state,
            "winner": winner
        })
    except:
        return render(request, "auctions/listing.html", {
            "listing": listings,
            "bids": highBid(bids),
            "comments": comments
        })
    else:
        return render(request, "auctions/error.html", {
            "error": "-This listing does not exist"
        })

# Register new bid/comment, update watchlist, close auction       
def newInput(request):
    # Get data from POST request and current listing
    data = request.POST
    listing = Listing.objects.get(id=data["item"])
    user = User.objects.get(id=request.user.id)
    # Place new bid
    if "bidButton" in request.POST:        
        form = newBid(data)
        if form.is_valid():
            allBids = Bid.objects.all()
            thisBid = form["newBid"].value()
            highestBid = highBid(allBids)
            # Only allows a bid to be placed if it's higher than any other already placed
            if float(thisBid) > float(highestBid[listing.id]) and float(thisBid) > listing.startingBid:
                f = Bid(user = user, product = listing, bid = thisBid)            
                f.save()
                return redirect("listing", data["item"])
            else:
                return render(request, "auctions/error.html", {
                    "error": "-Your bid is lower than all already placed"
                })
    # Add new comment
    elif "commentButton" in request.POST:
        form = newComment(data)
        if form.is_valid():
            f = Comment(author = user, product = listing, comment = form["newComment"].value())
            f.save()
            return redirect("listing", data["item"])
    # Add or remove listing from user's watchlist
    elif "watchlistState" in request.POST:
        state = int(data["watchlistState"])
        if state == 0:
            f = Wish(user = user, wishlist = listing)
            f.save()
        else:
            f = Wish.objects.get(user = user, wishlist = listing)
            f.delete()
        return redirect("listing", data["item"])
    # Close auction
    elif "closeAuction" in request.POST:
        listing.state = False
        listing.save()
        return redirect("listing", data["item"])
    else:
        return render(request, "auctions/error.html")

# Show user's watchlist
def watchlist(request):   
    user = User.objects.get(id=request.user.id)
    watch = Wish.objects.filter(user=user)
    bids = Bid.objects.all()
    return render(request, "auctions/watchlist.html", {
        "watchlist": watch,
        "highestBids": highBid(bids)
    })

# Show all categories
def category(request, category):
    roster = CATEGORY_CHOICES[1:]
    if category == "all":   
        return render(request, "auctions/categories.html", {
            "categories": roster,
            "check": True
        })
    # Show selected category
    else:
        selectedListings = Listing.objects.filter(category=category, state=True)
        bids = Bid.objects.all()
        if selectedListings:
            return render(request, "auctions/categories.html", {
                "listings": selectedListings,
                "highestBids": highBid(bids),
                "h1": category
            })
        # No listing in this specific category
        else:
            return render(request, "auctions/error.html", {
                "error": "-This category is currently empty"
            })