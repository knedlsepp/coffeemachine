from django.shortcuts import render
from django.http import HttpResponse
from coffeelist.models import *
from django.db.models import Avg, Sum, Count, Value
from django.db.models.functions import Coalesce
from django.contrib.auth.models import User
import json
from django.http import JsonResponse

import pandas as pd


def get_user_totals():
    user_deposit = {
        user.pk: user.deposits
        for user in User.objects.annotate(
            deposits=Coalesce(Sum('deposit__euros'), Value(0.)))
    }
    response = [{
        'pk': user.pk,
        'username': user.username,
        'full_name': '{} {}'.format(user.first_name, user.last_name),
        'total_deposits': user_deposit[user.pk],
        'total_purchases': user.total_purchases,
        'balance': user_deposit[user.pk] - user.total_purchases,
    } for user in User.objects.annotate(
        total_purchases=Coalesce(
            Sum('tag__purchase__price__euros'), Value(0.)))]

    df = pd.DataFrame(response)
    df.set_index('pk', inplace=True)
    return df


def index(request):
    df = get_user_totals()
    print(df)
    response = df[[
        'full_name',
        'total_deposits',
        'total_purchases',
        'balance',
    ]].to_html()
    return HttpResponse(response)
