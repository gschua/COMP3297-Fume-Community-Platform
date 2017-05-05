"""vapoursite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from .views import (main_view, game_view, myGames_view, view_tags, view_by_tag)
from .views import (delete_tag, manage_featured_games)
from accounts.views import (login_view, register_view, logout_view, change_email_view)
from cart.views import (cart_view, delete_from_cart, empty_cart, checkout)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^$', main_view, name='main'),
    url(r'^register/', register_view, name='register'),
    url(r'^login/$', login_view, name='login'),
    url(r'^accounts/login/$', login_view, name='login'),
    url(r'^logout/', logout_view, name='logout'),

    url(r'^accounts/change_email/$', change_email_view, name='change_email'),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

    url(r'^game/(?P<game_id>\d+)/', game_view, name='game'),
    url(r'^game/delete-tag/(?P<game_id>\d+)/(?P<tag_id>\d+)/', delete_tag, name='deleteTag'),
	#url(r'^game/addgame/(?P<game_id>\d+)/(?P<member_id>\d+)/', addtocart_view, name='addtocart'),

    url(r'^cart/(?P<member_id>\d+)/', cart_view, name='cart'),
    url(r'^cart/delete/(?P<transaction_id>\d+)', delete_from_cart, name='delFromCart'),
    url(r'^cart/empty/', empty_cart, name='emptyCart'),
    url(r'^cart/checkout/', checkout, name='checkout'),

    url(r'^myGames/(?P<member_id>\d+)/', myGames_view, name='myGames'),

    url(r'^tag/$', view_tags, name='viewTags'),
    url(r'^tag/(?P<tag_name>.+)/', view_by_tag, name='viewGamesByTag'),

    url(r'^manage/featured_games/$', manage_featured_games, name='manageFeaturedGames'),
    url('', include('social.apps.django_app.urls', namespace='social')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# For some reason, delete_from_cart, empty_cart, checkout all completely break if you change url(r'^cart/(?P<member_id>\d+)/',...) to url(r'^cart/',...), so even though its technically not needed just pass the member ID anyway
