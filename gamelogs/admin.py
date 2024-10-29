from django.contrib import admin

from .models import Publisher, Game, Review, User, Wishlist

admin.site.register(Publisher)
admin.site.register(Game)
admin.site.register(Review)
admin.site.register(User)
admin.site.register(Wishlist)