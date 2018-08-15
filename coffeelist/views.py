from django.shortcuts import render
from django.http import HttpResponse
from coffeelist.models import *
from django.db.models import Avg, Sum, Count
from django.contrib.auth.models import User
import json
from django.http import JsonResponse

import pandas as pd


def index(request):

    user_deposit = {
        user.pk: user.deposits
        for user in User.objects.annotate(deposits=Sum('deposit__euros'))
    }
    response = [{
        'pk': user.pk,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'total_deposits': user_deposit[user.pk],
        'total_purchases': user.total_purchases,
        'balance': user_deposit[user.pk] - user.total_purchases,
    } for user in User.objects.annotate(
        total_purchases=Sum('tag__purchase__price__euros'))]

    df = pd.DataFrame(response)
    response = df[[
        'first_name', 'last_name', 'balance',
        'total_deposits', 'total_purchases'
    ]].to_html()
    return HttpResponse(response)
