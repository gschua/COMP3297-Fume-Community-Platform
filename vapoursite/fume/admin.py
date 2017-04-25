from django.contrib import admin
from .models import Publisher, Genre, Platform, Game, Member, Transaction, Tag, Review, Reward

admin.site.register(Publisher)
admin.site.register(Genre)
admin.site.register(Platform)
admin.site.register(Game)
admin.site.register(Member)
admin.site.register(Transaction)
admin.site.register(Tag)
admin.site.register(Review)
admin.site.register(Reward)
