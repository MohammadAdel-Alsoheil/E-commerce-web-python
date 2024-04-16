from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *


from .models import User


def create(request):

    if request.user.is_authenticated:
        
        if request.method == "GET":
            return render(request, "auctions/create.html",{
                "cats": Category.objects.all()
            })
        
        
        
        username = request.user
        title = request.POST["title"]
        price = request.POST["price"]
        description = request.POST["description"]
        image = request.POST["image"]
        category = request.POST["category"]

        amount = Bids(amount=float(price), user = request.user)
        amount.save()
        cat = Category.objects.get(categoryName=category)      
        

        row = listing(title=title, image=image,description=description,price=amount,owner=username, category=cat)
        row.save()

        return HttpResponseRedirect(reverse("index"))
    
    return render(request, "auctions/login.html", {
                "message": "Forbidden access, please login"
            })


def watchlist(request):
    if request.user.is_authenticated:
        return render(request, "auctions/watchlist.html",{
            "items": Watchlist.objects.filter(user=request.user)
        })


def index(request):
    items = listing.objects.all()


    return render(request, "auctions/index.html",{
        "objects": items
    })


def didIwin(request):

    items = listing.objects.filter(isActive=False).all()

    return render(request, "auctions/didIwin.html",{
        "Won_Items":items
    })

def item(request, id):

    if request.user.is_authenticated:
        
        item = listing.objects.get(pk=id)

        if item.isActive:

            if request.method =="POST":

                    if 'listing' in request.POST:
                        l = request.POST['listing']

                        if Watchlist.objects.filter(user=request.user, watchlist=listing.objects.get(id=l)).exists() :
                            Watchlist.objects.filter(user=request.user,  watchlist=listing.objects.get(id=l)).delete()
                        else:
                            user_instance = request.user  
                            listing_instance = listing.objects.get(pk=l)

                            watchlist_instance = Watchlist(user=user_instance)
                            watchlist_instance.save()
                            watchlist_instance.watchlist.add(listing_instance)

                    elif 'comment' in request.POST:
                        text = request.POST['comment']

                        Comment(owner=request.user, text=text, item = listing.objects.get(id=id)).save()

                    elif 'CloseBiding' in request.POST:
                        
                        item.isActive = False

                        item.save()

                        return redirect(request.path)


                    elif 'bidding' in request.POST:
                        

                        amount = request.POST['bidding']

                        if float(amount)<float(item.price.amount):
                            
                            return render(request, "auctions/item.html",{
                                "item":item,
                                "added":Watchlist.objects.filter(user=request.user, watchlist=listing.objects.get(id=id)).exists(),
                                "comments": Comment.objects.filter(item=listing.objects.get(id=id)),
                                "user": request.user,
                                "message": f"please enter a number larger than the current bid {item.price}$"
                            })
                        else:
                            newBid = Bids(user=request.user, amount=amount)
                            newBid.save()

                            item.price = newBid
                            item.num_of_bids+=1
                            item.save()






            
            return render(request, "auctions/item.html",{
                "item":item,
                "added":Watchlist.objects.filter(user=request.user, watchlist=listing.objects.get(id=id)).exists(),
                "comments": Comment.objects.filter(item=listing.objects.get(id=id)),
                "user": request.user,
                "message":""
            })
        

        else:
            if request.user==item.price.user:
                return render(request, "auctions/item.html",{

                "item":item,
                "added":Watchlist.objects.filter(user=request.user, watchlist=listing.objects.get(id=id)).exists(),
                "comments": Comment.objects.filter(item=listing.objects.get(id=id)),
                "user": request.user,
                "message":""

                })
            return render(request, "auctions/non_active.html")
        
    return render(request, "auctions/login.html", {
            "message": "Please login before you proceed."
        })


def category(request):
    if request.user.is_authenticated:
        return render(request, "auctions/category.html",{
            "categories": Category.objects.exclude(categoryName="None").all()
        })

    return render(request, "auctions/login.html", {
            "message": "Please login before you proceed."
        })

def OneCat(request, name):
    if request.user.is_authenticated:
        if name!='None':
            return render(request, "auctions/OneCat.html",{
                "cat":name,
                "objects": listing.objects.filter(category=Category.objects.get(categoryName=name))
            })
        else:
            return render(request, "auctions/category.html",{
            "categories": Category.objects.exclude(categoryName="None").all()
        })

    
    return render(request, "auctions/login.html", {
            "message": "Please login before you proceed."
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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
