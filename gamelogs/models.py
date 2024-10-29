import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
from django.db import models


class Publisher(models.Model):
    name = models.CharField(max_length=100)
    creation_date = models.DateField()

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    genre = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)  # Allows for prices up to 9999.99
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name="games")

    def __str__(self):
        return self.name


class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    join_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.username


class Review(models.Model):

    class Meta:
        unique_together = (('user', 'game'),)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField()  # Can also use a more constrained field if you want to limit to 1-5, etc.
    date = models.DateField(auto_now=True)  # Update to current date when updated

    def __str__(self):
        return f"Review by {self.user} for {self.game}"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="wishlisted_by")
    add_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} added {self.game} to wishlist"
