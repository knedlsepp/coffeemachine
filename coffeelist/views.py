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
        user.id: user.deposits
        for user in User.objects.annotate(deposits=Sum('deposit__euros'))
    }
    response = [{
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'balance': user_deposit[user.id] - user.expenses
    } for user in User.objects.annotate(
        expenses=Sum('tag__purchase__price__euros'))]
    return JsonResponse(response, safe=False)
