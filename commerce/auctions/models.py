from django.contrib.auth.models import AbstractUser
from django.db import models

CATEGORY_CHOICES = [
    ('None', 'Select a category'),
    ('Fashion', 'Fashion'),
    ('Eletronics & DIY', 'Eletronics & DIY'),
    ('Personal Care', 'Personal Care'),
    ('Furniture & Appliances', 'Furniture & Appliances')
]

class User(AbstractUser):
    pass

class Listing(models.Model):
    objects = models.Manager()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    startingBid = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=700)
    image = models.URLField(max_length=300)
    creationTime = models.DateTimeField()
    category = models.CharField(max_length=22 ,choices=CATEGORY_CHOICES, blank=False, default='None')
    state = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.owner}'s {self.title}"

class Comment(models.Model):
    objects = models.Manager()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.author}'s comment in {self.product}"

class Bid(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user}'s {self.bid} bid on {self.product}"

class Wish(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wishlist = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.wishlist} is in {self.user}'s watchlist" 