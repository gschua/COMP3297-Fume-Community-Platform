from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )
from fume.models import Member, Reward, Transaction
from django.utils import timezone

def cart_view(request, member_id):

    user = request.user
    cart = Transaction.objects.filter(member=user).filter(is_purchased=False)

    if request.POST.get('addReward'):
        entry = request.POST.get('addReward')
        entry = Transaction.objects.get(id=entry)
        if (user.get_reward_count() > entry.rewards_used and entry.rewards_used < 10):
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
