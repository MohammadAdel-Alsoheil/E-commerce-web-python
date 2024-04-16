from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

class Category(models.Model):
    categoryName = models.CharField(max_length=60)

    def __str__(self):
        return self.categoryName
    

class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, related_name="bidder")
    amount = models.FloatField()

    def __str__(self):
        return str(self.amount)


class listing(models.Model):

    title = models.CharField(max_length=30)
    image = models.CharField(max_length=1200)
    description = models.CharField(max_length=200)
    price = models.ForeignKey(Bids,on_delete=models.CASCADE,blank=True, related_name='bid')
    num_of_bids = models.IntegerField(default=0)
    isActive = models.BooleanField(default= True)
    dateAndTime = models.TimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, related_name= "user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, related_name="category", default="None")

    def __str__(self):
        return f"{self.title}"
    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, related_name="watchlist_user")
    watchlist = models.ManyToManyField(listing)

    def __str__(self):
        listings = ', '.join([listing.title for listing in self.watchlist.all()])
        return f"{listings}"
    

class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, related_name="commentor")
    item = models.ForeignKey(listing,on_delete=models.CASCADE, blank=True, related_name="item")
    text = models.CharField(max_length=600)
    dateAndTime =  models.TimeField(default=timezone.now)


    def __str__(self):
        return f"owner: {self.owner}, on item: {self.item}"
    

    


    
