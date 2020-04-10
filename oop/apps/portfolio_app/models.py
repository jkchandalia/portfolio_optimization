import re
import requests

from . import data
from apps.login_app.models import User
from django.db import models


# Create your models here.
class OptionsManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        return errors


class Option(models.Model):
    equity = models.CharField(max_length=255)
    strike = models.IntegerField()
    exp_date = models.DateField()
    option_type = models.CharField(max_length=255)
    bid = models.FloatField()
    ask = models.FloatField()
    mark = models.FloatField()
    delta = models.FloatField()
    theta = models.FloatField()
    gamma = models.FloatField()
    vega = models.FloatField()
    equity_price = models.FloatField()
    flavor = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = OptionsManager()

    def _calculate_margin(self):
        # http://www.cboe.com/LearnCenter/pdf/margin2-00.pdf
        if self.option_type == "CALL":
            margin = max(100 * (self.mark + self.equity_price*.15 + min(0,self.equity_price - self.strike)),10*self.equity_price+self.mark*100)
        elif self.option_type == "PUT":
            margin = max(100 * (self.mark + self.equity_price*.15 + min(0,self.strike-self.equity_price)),10*self.strike+self.mark*100)
        return margin

    def _update_w_api_data(self):
        self.api_data = requests.get(url = data.endpoint, params = self.query_params).json()
        self._parse_api_data()
        self.save()

    def _parse_api_data(self):
        self.equity_price = self.api_data['underlyingPrice']
        if self.option_type == 'CALL':
            data=self.api_data['callExpDateMap']
        elif self.option_type == 'PUT':
            data=self.api_data['putExpDateMap']

        for date_key in data:
            for price_key in data[date_key]:
                # print(price_key)
                values=data[date_key][price_key][0]
                # print(values.keys())
                self.symbol = values['symbol']
                self.description = values['description']
                self.bid = values['bid']
                self.ask = values['ask']
                self.mark = values['mark']
                self.delta = values['delta']
                self.theta = values['theta']
                self.gamma = values['gamma']
                self.vega = values['vega']
                self.daysToExpiration = values['daysToExpiration']
                    
    @property
    def margin(self):
        return self._calculate_margin()

    @property
    def query_params(self):
        params={"apikey": data.client_id,
        "symbol": self.equity,
        "contractType": self.option_type.upper(),
        "strike": self.strike,
        "fromDate": self.exp_date,
        "toDate": self.exp_date}
        return params

    def update_data(self):
        self._update_w_api_data()


class MarginableEquity(models.Model):
    amount = models.IntegerField(default=0)
    user = models.OneToOneField(User, related_name="margin_available", default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class QuantityOptions(models.Model):
    option_count = models.IntegerField(default=0)
    user = models.ForeignKey(User, related_name="number_owned", default=None)
    option = models.ForeignKey(Option, related_name="option_owned", default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DailySummary(models.Model):
    summary_on = models.BooleanField(default=False)
    endpoint = models.CharField(max_length=255, default=None)
    endpoint_type = models.CharField(max_length=255, default=None)
    user = models.OneToOneField(User, related_name="summary_on")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    