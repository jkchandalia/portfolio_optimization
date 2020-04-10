import bcrypt
import json
import requests

from . import data, helper
from apps.login_app.models import *
from apps.portfolio_app.models import *
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse


def send_daily_summary():
  pass

def send_slack_msg():
    users = User.objects.filter(email='jkchandalia@gmail.com')
    for user in users:
        portfolio = helper.make_portfolio(user)
        instructions = helper.make_trade_instructions(portfolio)
        slack_data = {'text': f"Trading instructions for {user.first_name}. " + "\n".join(instructions)}

        response = requests.post(
        data.slack_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
        )
        if response.status_code != 200:
            raise ValueError(
                'Request to slack returned an error %s, the response is:\n%s'
                % (response.status_code, response.text)
            )
