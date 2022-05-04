from socket import SO_LINGER
from xml.parsers.expat import model
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
from django.db import models
from IPython.display import display

# Create your models here.

class BoxScoreHitting(models.Model):
    
    NAME                = models.CharField(max_length=100, null=True)
    TEAM                = models.CharField(max_length=100, null=True)
    DATE                = models.IntegerField(null=True)
    SIDE                = models.CharField(max_length=100, null=True)
    POSITION            = models.CharField(max_length=100, null=True)
    AB                  = models.IntegerField(null=True)
    R                   = models.IntegerField(null=True)
    H                   = models.IntegerField(null=True)
    RBI                 = models.IntegerField(null=True)
    BB                  = models.IntegerField(null=True)
    SO                  = models.IntegerField(null=True)
    PA                  = models.IntegerField(null=True)
    BA                  = models.FloatField(null=True)
    OBP                 = models.FloatField(null=True)   
    SLG                 = models.FloatField(null=True)
    OPS                 = models.FloatField(null=True)
    PITCHES             = models.IntegerField(null=True)
    STRIKES             = models.IntegerField(null=True)
    WPA                 = models.FloatField(null=True)
    ALI                 = models.FloatField(null=True)
    RE24                = models.FloatField(null=True)

class BoxScorePitching(models.Model):
    pass
