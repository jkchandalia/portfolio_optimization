import datetime
import requests

from . import data
from collections import deque


class Portfolio:
    def __init__(self, name):
        self.name = name
        self.options = []

    def add_option(self, option):
        self.options.append(option)
        return self
    
    def remove_option(self, option):
        self.options.remove(option)
        return self

    def _calculate_strangle_margin(self, option_call, option_put):
        return min(option_call.margin+100*option_put.mark,option_put.margin+100*option_call.mark )

    def _calculate_margin(self):
        margin = 0
        calls = deque()
        puts = deque()
        counter_put = 0
        counter_call = 0
        for option in self.options:
            if option.option_type == 'CALL':
                calls.append(option)
            elif option.option_type == 'PUT':
                puts.append(option)
        for i in range(min(len(calls), len(puts))):
            margin_delta = self._calculate_strangle_margin(calls.popleft(),puts.pop())
            margin += margin_delta
        if puts:
            while puts:
                margin += puts.pop().margin
        else:
            while calls:
                margin += calls.pop().margin
        margin = margin * 2
        return int(round(margin,-2))

    @property
    def margin(self):
        return self._calculate_margin()

    @property
    def liability(self):
        return self._calculate_liability()

    def _calculate_liability(self):
        liability = 0
        for option in self.options:
            liability = liability + 100 * option.mark
        return liability

    @property
    def portfolio_summary(self):
        #organize by equity symbol and then calls/puts then all else
        #maybe another view with strangle pairs
        return 'Summary'
        
    @property
    def instructions_summary(self):
        pass
        
    def update_data(self):
        for option in self.options:
            option.update_data() 
            option.save() 

    def send_SMS(self):
        pass

    def send_slack_msg(self):
        pass    

def make_portfolio(user):
    my_portfolio = Portfolio('my_portfolio')
    counts=user.number_owned.all()
    
    for count in counts:
        for i in range(count.option_count):
            my_portfolio.add_option(count.option)
    return my_portfolio
    
def parse_api_data(api_data, params):
    output = {}
    output['equity_price'] = api_data['underlyingPrice']
    if params['contractType'] == 'CALL':
        option_data=api_data['callExpDateMap']
    elif params['contractType'] == 'PUT':
        option_data=api_data['putExpDateMap']

    for date_key in option_data:
        for price_key in option_data[date_key]:
            values=option_data[date_key][price_key][0]
            output['symbol'] = values['symbol']
            output['description'] = values['description']
            output['bid'] = values['bid']
            output['ask'] = values['ask']
            output['mark'] = values['mark']
            output['delta'] = values['delta']
            output['theta'] = values['theta']
            output['gamma'] = values['gamma']
            output['vega'] = values['vega']
            output['equity']=params['symbol']
            output['strike']=params['strike']
            output['exp_date']=params['fromDate']
            output['option_type']=params['contractType']
            output['flavor']='european'
            output['daysToExpiration']=values['daysToExpiration'] 
        return output

def get_market_data(params):
    content = requests.get(url = data.endpoint, params = params)
    api_data=content.json()
    if api_data['status'] == 'FAILED':
        return False
    elif api_data['status'] == 'SUCCESS':
        output = parse_api_data(api_data, params)
    return output

def make_trade_instructions(portfolio):
    msg = []
    msg.append(f'Net portfolio liability is {portfolio.liability}')
    calls = 0
    puts = 0
    for option in portfolio.options:
        if option.option_type == 'CALL':
            calls += 1
        elif option.option_type == 'PUT':
            puts += 1
    msg.append(f'Number of calls is {calls}; number of puts is {puts}.')
    
    for option in portfolio.options:
        date_delta = datetime.datetime.strptime(str(option.exp_date)  , '%Y-%m-%d') - datetime.datetime.now()
        days_to_expiry = date_delta.days
        #date-related instructions
        if datetime.datetime.strptime(str(option.exp_date)  , '%Y-%m-%d') - datetime.datetime.now()<datetime.timedelta(days=7):
            msg.append(f'The option {option.symbol} needs to be rolled or closed within the next {days_to_expiry} days. It has a value of {option.mark}')
        if  datetime.datetime.now() > datetime.datetime.strptime(str(option.exp_date)  , '%Y-%m-%d'):
            msg.append(f'The option {option.symbol} has expired and portfolio needs to be updated.')
        #danger-zone instructions
        if option.option_type=='CALL' and option.strike<option.equity_price:
            msg.append(f'For call option {option.symbol}, strike has been breached.In the money by {option.equity_price-option.strike}')
        if option.option_type=='PUT' and option.strike>(option.equity_price*0.98):
            msg.append(f'For put option {option.symbol}, strike is within danger range. Time to roll.')
        elif option.option_type=='PUT' and option.strike>(option.equity_price*0.9):
            msg.append(f'For put option {option.symbol}, strike is within 10% of current equity price. Consider rolling.')

    trade_instructions = " ".join(msg) 
    if not(msg):
        msg.append("No changes needed.")
    return msg

def update_market_data(portfolio):
    for option in portfolio.options:
        output = get_market_data(option.query_params)
        option.update(output)
        option.save()
    

