import json

from .apps import PredictAppConfig 
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView


class call_model(APIView):

    def get(self,request):
        if request.method == 'GET':
            days_to_expiry =  request.GET.get('days_to_expiry')
            # predict method used to get the prediction
            response = PredictAppConfig.model.predict([[int(days_to_expiry)]])
            # returning JSON response
            return HttpResponse(json.dumps(response[0]), content_type="application/json")