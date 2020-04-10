import bcrypt
import json
import requests

from . import data
from apps.login_app.models import User
from apps.portfolio_app.helper import *
from apps.portfolio_app.models import *
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse


def plot_options(request):
    user = User.objects.get(id=request.session['userid'])
    my_portfolio = make_portfolio(user)
    out = []
    for option in my_portfolio.options:
        datapoint={}
        datapoint['exp_date'] = option.exp_date.strftime("%y-%m-%d")
        datapoint['strike'] = option.strike
        if option.option_type=='CALL':
            datapoint['color']='brown'
        else:
            datapoint['color']='green'
        out.append(datapoint)
    return HttpResponse(json.dumps(out), content_type="application/json")

def index(request):
    return render(request, 'portfolio_app/index.html')

def main(request):
    user = User.objects.get(id=request.session['userid'])
    if not(hasattr(user, 'margin_available')):
        MarginableEquity.objects.create(amount=0,user=user)
    
    my_portfolio = make_portfolio(user)
    
    context = {
        'user': user,
        'portfolio': my_portfolio,
    }

    return render(request, 'portfolio_app/portfolio.html', context)

def validate_option(request):
    f = request.POST
    params={"apikey": data.client_id,
            "symbol": f["equity"],
            "contractType": f["type"].upper(),
            "strike": f["strike"],
            "fromDate": f["exp_date"],
            "toDate":f["exp_date"]}
            
    option_exists = Option.objects.filter(
        equity=params['symbol'],
        strike=params['strike'],
        exp_date=params['fromDate'],
        option_type=params['contractType']
    )
    user=User.objects.get(id=request.session['userid'])

    if option_exists:
        option = option_exists[0]
        option_count = QuantityOptions.objects.filter(user=user, option=option)
        if option_count:
            count = option_count[0]
            count.option_count += int(f['quantity'])
            count.save()
            return redirect("/portfolio/options")
        else:
            QuantityOptions.objects.create(
                option_count=int(f['quantity']),
                user=user,
                option=option)
            return redirect("/portfolio/options")
    else:
        output = get_market_data(params)
        if output:
            new_option = Option.objects.create(
                equity=params['symbol'],
                strike=output['strike'],
                exp_date=output['exp_date'],
                option_type=output['option_type'],
                bid=output['bid'],
                ask=output['ask'],
                mark=output['mark'],
                delta=output['delta'],
                theta=output['theta'],
                gamma=output['gamma'],
                vega=output['vega'],
                equity_price=output['equity_price'],
                flavor=output['flavor'],
                desc=output['description'],
                symbol=output['symbol'])
            QuantityOptions.objects.create(option_count=int(f['quantity']), user=user, option=new_option)

            return redirect("/portfolio/options")
        else:
            messages.error(request, "The option was not found")
            return redirect("/portfolio/options")

def update_margin_avail(request):
    user=User.objects.get(id=request.session['userid'])
    margin_avail = user.margin_available
    margin_avail.amount=request.POST['margin_avail']
    margin_avail.save()
    return redirect("/portfolio/main")

def update_portfolio(request):
    user = User.objects.get(id=request.session['userid'])
    my_portfolio = make_portfolio(user)
    context = {
        'user': user,
        'portfolio': my_portfolio,
    }
    return render(request, "portfolio_app/options.html", context)

def remove_option(request):
    f=request.POST
    user = User.objects.get(id=request.session['userid'])
    if 'to_remove' in f:
        counts=user.number_owned.all()
        option = Option.objects.get(id=f['to_remove'])
        for count in counts:
            if option==count.option:
                if count.option_count==1:
                    count.delete()
                else:
                    count.option_count = count.option_count - 1
                    count.save()
    my_portfolio = make_portfolio(user)
    context = {
        'user': user,
        'portfolio': my_portfolio,
    }
    return render(request, "portfolio_app/options.html", context)

def instructions(request):
    user = User.objects.get(id=request.session['userid'])
    my_portfolio = make_portfolio(user)
    instructions = make_trade_instructions(my_portfolio)
    context = {
        'instructions':instructions,
    }
    return render(request, "portfolio_app/instructions.html", context)

def analysis(request):
    return render(request, "portfolio_app/analysis.html")

def bollinger_band(request):
    pass

def margin_available(request):
    pass

def simulate_shock(request):
    user = User.objects.get(id=request.session['userid'])
    my_portfolio = make_portfolio(user)
    print(user.margin_available.amount*.9)
    user.margin_available.amount = user.margin_available.amount*.9
    print(user.margin_available.amount)
    # user.save()
    print(my_portfolio.margin)
    for option in my_portfolio.options:
        option.mark = option.mark*1.1
    print(my_portfolio.margin)

    context = {
        'user': user,
        'portfolio': my_portfolio,
        'shock':'true',
    }
    
    print(context['portfolio'].margin)
    return render(request, 'portfolio_app/portfolio.html', context)

def send_slack_msg(request):
    user = User.objects.get(id=request.session['userid'])
    portfolio = make_portfolio(user)
    instructions = make_trade_instructions(portfolio)
    slack_data = {'text': f"Trading instructions for {user.first_name}. " + " ".join(instructions)}

    response = requests.post(
    data.slack_url, data=json.dumps(slack_data),
    headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )
    return redirect("/portfolio/options")

def send_sms(request):
    return redirect("/portfolio/options")

def update_market_data(request):
    user = User.objects.get(id=request.session['userid'])
    my_portfolio = make_portfolio(user)
    my_portfolio.update_data()
    return redirect("/portfolio/main")

def toggle_summary(request):
    user=User.objects.get(id=request.session['userid'])
    user.summary_on.summary_on = not(user.summary_on.summary_on)
    user.save()