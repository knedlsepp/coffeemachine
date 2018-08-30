from django.shortcuts import render
from django.http import HttpResponse
from coffeelist.models import *
from django.db.models import Avg, Sum, Count, Value
from django.db.models.functions import Coalesce
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
import django_tables2 as tables
import pandas as pd


def get_user_totals():
    user_deposit = {
        user.pk: user.deposits
        for user in User.objects.annotate(
            deposits=Coalesce(Sum('deposit__euros'), Value(0.)))
    }
    user_total_coffees = {
        user.pk: user.total_coffees
        for user in User.objects.annotate(
            total_coffees=Coalesce(Count('tag__purchase'), Value(0.)))
    }
    response = [{
        'pk': user.pk,
        'username': user.username,
        'full_name': '{} {}'.format(user.first_name, user.last_name),
        'total_deposits': user_deposit[user.pk],
        'total_purchases': user.total_purchases,
        'total_coffees': user_total_coffees[user.pk],
        'balance': user_deposit[user.pk] - user.total_purchases,
    } for user in User.objects.annotate(
        total_purchases=Coalesce(
            Sum('tag__purchase__price__euros'), Value(0.)))]

    df = pd.DataFrame(response)
    df.set_index('pk', inplace=True)
    return df


class CoffelistTable(tables.Table):
    full_name = tables.Column()
    total_coffees = tables.Column()
    total_purchases = tables.Column()
    total_deposits = tables.Column()
    balance = tables.Column()

    class Meta:
        template_name = 'django_tables2/bootstrap.html'


def index(request):
    df = get_user_totals()
    response = df[[
        'full_name',
        'total_coffees',
        'total_purchases',
        'total_deposits',
        'balance',
    ]].to_html()
    table = CoffelistTable(df.to_dict(orient='records'))
    return render(request, 'coffeelist/coffeelist.html', {'table': table})
