import html
import os
import pickle
import sklearn

from django.apps import AppConfig


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
class PredictAppConfig(AppConfig):
    name = 'predict_app'
    MODEL_PATH = os.path.join(BASE_DIR, 'predict_app/model/preliminary_options_decay.sav')
    model = pickle.load(open(MODEL_PATH, 'rb'))

