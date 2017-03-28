from django.contrib import admin

# Register your models here.
from .models import Member, Game, Transaction, Publisher, Review, Reward, Genre, Tag, ShoppingCart, Admin

admin.site.register(Member)
admin.site.register(Game)
admin.site.register(Transaction)
admin.site.register(Publisher)
admin.site.register(Reward)
admin.site.register(Review)
admin.site.register(Genre)
admin.site.register(Tag)
admin.site.register(ShoppingCart)
admin.site.register(Admin)