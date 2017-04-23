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

from fume.models import Member, Game, Reward, Transaction, Tag, MemberTag, Platform
from fume.forms import AddToCartForm, NewTagForm


def main_view(request):
    user = request.user
    user_rewards = []
    if user.is_authenticated:
        user_rewards = Reward.objects.filter(member=user).filter(Q(status='act')|Q(status='car')).order_by('expiry_date')
    template = loader.get_template('vapoursite/main.html')
    context = {
        'user': user,
        'featured': Game.objects.filter(featured=True),
        'user_rewards': user_rewards,
    }
    return HttpResponse(template.render(context, request))


def game_view(request, game_id):

    member = request.user
    game = Game.objects.get(id=game_id)
    purchased = []
    member_tags = []
    if member.is_authenticated:
        purchased = Transaction.objects.filter(member=member).filter(game=game).filter(is_purchased=True)
        member_tags = MemberTag.objects.filter(member=member).filter(game=game)

    platform_used = Transaction.objects.filter(member=member).filter(game=game).values_list('platform', flat=True)
    platform_used = Platform.objects.filter(id__in=platform_used)
    cartform = AddToCartForm(request.POST or None)
    if cartform.is_valid():
        x = cartform.cleaned_data.get('platform')
        if not(x in platform_used) and x in game.platforms.all():
            cart_entry = cartform.save(commit=False)
            cart_entry.member = member
            cart_entry.game = game
            cart_entry.platform = x
            cart_entry.price = game.price
            cart_entry.rewards_used = 0
            cart_entry.save()
            return HttpResponseRedirect('/game/'+game_id+'/')

    member_game_tags = member_tags.values_list('tag__name', flat=True)
    all_tags = Tag.objects.all().values_list('name', flat=True)
    game_tags = game.tag_set.all().values_list('name', flat=True)
    newtagform = NewTagForm(request.POST or None)
    if newtagform.is_valid():
        x = newtagform.cleaned_data.get('name')
        if x in member_game_tags:
            pass #add some error message
        elif x in game_tags:
            new_memtag = MemberTag()
            new_memtag.member = member
            new_memtag.game = game
            new_memtag.tag = Tag.objects.get(name=x)
            new_memtag.save()
        elif x in all_tags:
            old_tag = Tag.objects.get(name=x)
            old_tag.games.add(game)
            old_tag.save()
            new_memtag = MemberTag()
            new_memtag.member = member
            new_memtag.game = game
            new_memtag.tag = old_tag
            new_memtag.save()
        else:
            new_tag = newtagform.save()
            new_tag.name = x
            new_tag.games.add(game)
            new_memtag = MemberTag()
            new_memtag.member = member
            new_memtag.game = game
            new_memtag.tag = new_tag
            new_memtag.save()
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


def cart_view(request, member_id):

    user = request.user
    cart = Transaction.objects.filter(member=user).filter(is_purchased=False)

    if request.POST.get('addReward'):
        entry = request.POST.get('addReward')
        entry = Transaction.objects.get(id=entry)
        if (user.get_reward_count() > 0 and entry.rewards_used < 10):
            entry.rewards_used += 1
            entry.save()
            reward = user.reward_set.filter(status='act').earliest('expiry_date')
            reward.status = 'car'
            reward.save()

    if request.POST.get('removeReward'):
        entry = request.POST.get('removeReward')
        entry = Transaction.objects.get(id=entry)
        reward = user.reward_set.filter(status='car')
        if (entry.rewards_used > 0 and reward):
            entry.rewards_used -= 1
            entry.save()
            reward = reward.latest('expiry_date')
            reward.status = 'act'
            reward.save()

    reward_threshold = 100.0
    reward_total = 0
    total_pre_reward = 0.0
    total_post_reward = 0.0
    for entry in cart:
        reward_total += entry.rewards_used
        total_pre_reward += entry.price
        total_post_reward += entry.get_discount_price()
    reward_received = int(total_post_reward / reward_threshold)

    template = loader.get_template('vapoursite/cart.html')
    context = {
        'user': user,
        'cart': cart,
        'pretotal': total_pre_reward,
        'postotal': total_post_reward,
        'reward_tot': reward_total,
        'reward_rcv': reward_received,
    }

    return HttpResponse(template.render(context, request))


def delete_from_cart(request, transaction_id):
    t = Transaction.objects.get(id=transaction_id)
    rew = Reward.objects.filter(member=request.user).filter(status='car').order_by('-expiry_date')[:t.rewards_used]
    for r in rew:
        r.status = 'act'
        r.save()
    t.delete()
    return HttpResponseRedirect('/cart/' + str(request.user.id) +'/')


def empty_cart(request):
    cart = Transaction.objects.filter(member=request.user).filter(is_purchased=False)
    for transaction in cart:
        t = Transaction.objects.get(id=transaction.id)
        rew = Reward.objects.filter(member=request.user).filter(status='car').order_by('-expiry_date')[:t.rewards_used]
        for r in rew:
            r.status = 'act'
            r.save()
        t.delete()
    return HttpResponseRedirect('/cart/' + str(request.user.id) +'/')


def checkout(request):
    member = request.user
    cart = Transaction.objects.filter(member=member).filter(is_purchased=False)
    spending = member.acc_spending
    for t in cart:
        rew = Reward.objects.filter(member=member).filter(status='car').order_by('expiry_date')[:t.rewards_used]
        for r in rew:
            r.status = 'use'
            r.transaction = t
            r.save()
        t.is_purchased=True
        t.purchase_datetime = timezone.now()
        spending += t.get_discount_price()
        t.save()
    reward_threshold = 100.0
    while spending >= reward_threshold:
        spending -= reward_threshold
        new_reward = Reward()
        new_reward.member = member
        new_reward.save()
    member.acc_spending = spending
    member.save()
    return HttpResponseRedirect('/')


def delete_tag(request, game_id, member_tag_id):
    t1 = MemberTag.objects.get(id=member_tag_id)
    t2 = t1.tag
    g = t1.game
    t1.delete()
    if not t2.membertag_set.filter(game=g):
        t2.games.remove(g)
    if t2.membertag_set.count() == 0:
        t2.delete()
    return HttpResponseRedirect('/game/'+game_id+'/')


#redirected to login page if not logged in user tries to access this view
#@login_required(login_url='/login/')
#def loginmain_view(request):
#    if (request.user.is_authenticated())
#        return render(request, "vapoursite/main-loggedin.html", {'user': request.user})

# only deals with successful callback
#def callback(request):
#    if 
