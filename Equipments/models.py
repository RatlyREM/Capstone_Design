from django.db import models
from django.utils import timezone
from datetime import datetime
import Accounts.models

class Equipment(models.Model):
    model_name=models.CharField(max_length=50, primary_key=True)
    name=models.CharField(max_length=30, default=None)
    type=models.CharField(max_length=30, default=None)
    price=models.IntegerField(blank=True, null=True, default=0)
    repository=models.CharField(max_length=30, default=None)
    total_rent=models.IntegerField(blank=True, null=True, default=0)
    total_stock=models.IntegerField(blank=True, null=True, default=0)
    current_stock=models.IntegerField(blank=True, null=True, default=0)
    manufacturer= models.CharField(max_length=30, blank=True, null=True, default=None)
    recommend_count=models.IntegerField(blank=True, null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    recommend_user = models.ManyToManyField(Accounts.models.User, related_name='recommend_user', blank=True)

    class Meta:
        #managed = False
        db_table= 'equipment'

class Log(models.Model):
    u = models.ForeignKey('Accounts.User', on_delete=models.CASCADE, related_name='log_user_id')
    model_name = models.ForeignKey('Equipment', on_delete=models.CASCADE, db_column='model_name')
    rent_count= models.IntegerField(default=0)
    return_deadline = models.DateTimeField(blank= True, null= True, default= None)
    rent_requested_date = models.DateTimeField(blank= True, null= True, default= None)
    rent_accepted_date = models.DateTimeField(blank= True, null= True, default= None)
    return_requested_date = models.DateTimeField(blank= True, null= True, default= None)
    return_accepted_date = models.DateTimeField(blank= True, null= True, default= None)
    rent_price= models.IntegerField(blank=True, null=True, default= None)

    class Meta:
        #managed= False
        db_table = 'log'