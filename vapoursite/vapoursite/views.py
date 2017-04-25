from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )
from django.db.models import Sum, Q
from django.utils import timezone
from django.forms import modelformset_factory, TextInput, CheckboxInput

from fume.models import Member, Game, Reward, Transaction, Tag, Platform
from fume.forms import AddToCartForm, NewTagForm


def main_view(request):
    user = request.user
    user_rewards = []
    if user.is_authenticated:
        user_rewards = Reward.objects.filter(member=user).filter(Q(status='act')|Q(status='car')).order_by('expiry_date')
    template = loader.get_template('vapoursite/main.html')
    context = {
        'user': user,
        'featured': Game.objects.filter(featured=True).order_by('release_date'),
        'user_rewards': user_rewards,
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='/login/')
def game_view(request, game_id):

    member = request.user
    game = Game.objects.get(id=game_id)
    purchased = []
    member_tags = []
    if member.is_authenticated:
        purchased = Transaction.objects.filter(member=member).filter(game=game).filter(is_purchased=True)
        member_tags = Tag.objects.filter(member=member).filter(game=game)

    platform_used = Transaction.objects.filter(member=member).filter(game=game).values_list('platform', flat=True)
    platform_used = Platform.objects.filter(id__in=platform_used)
    cartform = AddToCartForm(request.POST or None)
    if cartform.is_valid():
        platform_choice = cartform.cleaned_data.get('platform')
        if not(platform_choice in platform_used) and platform_choice in game.platforms.all():
            cart_entry = cartform.save(commit=False)
            cart_entry.member = member
            cart_entry.game = game
            cart_entry.platform = platform_choice
            cart_entry.price = game.price
            cart_entry.rewards_used = 0
            cart_entry.save()
            return HttpResponseRedirect('/game/'+game_id+'/')

    newtagform = NewTagForm(request.POST or None)
    if newtagform.is_valid():
        new_name = newtagform.cleaned_data.get('name')
        if new_name in member_tags.values_list('name', flat=True):
            pass #add some error message
        else:
            new_tag = Tag()
            new_tag.name = new_name
            new_tag.member = member
            new_tag.game = game
            new_tag.save()
        return HttpResponseRedirect('/game/'+game_id+'/')

    template = loader.get_template('vapoursite/game.html')
    context = {
        'user': request.user,
        'game': game,
        'member_tags': member_tags,
        'purchased': purchased,
        'cartform': cartform,
        'newtagform': newtagform,
    }

    return HttpResponse(template.render(context, request))


@login_required(login_url='/login/')
def myGames_view(request, member_id):
    user = request.user
    myGames= Transaction.objects.filter(member=user).filter(is_purchased=True).order_by('-purchase_datetime')

    myGames_count = 0
    total_spending = 0.0
    total_reward_used = 0

    for entry in myGames:
        myGames_count += 1
        total_spending += entry.get_discount_price()
        total_reward_used += entry.rewards_used

    template = loader.get_template('vapoursite/myGames.html')
    context = {
        'user': user,
        'myGames': myGames,
        'spending': total_spending,
        'rewards': total_reward_used,
        'games_tot': myGames_count,
    }

    return HttpResponse(template.render(context, request))

def delete_tag(request, game_id, tag_id):
    Tag.objects.get(id=tag_id).delete()
    return HttpResponseRedirect('/game/'+game_id+'/')


def manage_featured_games(request):

	FeaturedGameFormSet = modelformset_factory(Game, fields=('title', 'featured'), widgets={'title': TextInput(attrs={'readonly': True}), 'featured': CheckboxInput(attrs={'required': False})}, extra=0)
	form=FeaturedGameFormSet(queryset= Game.objects.all(), initial=Game.objects.values('title', 'featured'))
	#formset=FeaturedGameFormSet(initial=[{'featured': game.featured, 'featured.label' : game.title} for game in games])
	if request.method == 'POST':
		form=FeaturedGameFormSet(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('')
	else:
		return render(request, 'vapoursite/manage.html', {'type': 'Featured games', 'form': form, 'user': request.user})


#redirected to login page if not logged in user tries to access this view
#@login_required(login_url='/login/')
#def loginmain_view(request):
#    if (request.user.is_authenticated())
#        return render(request, "vapoursite/main-loggedin.html", {'user': request.user})

# only deals with successful callback
#def callback(request):
#    if
