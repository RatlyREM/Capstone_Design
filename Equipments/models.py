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
    updated_at = models.DateTimeField(auto_now=True)

    recommend_user = models.ManyToManyField(Accounts.models.User, related_name='recommend_user', blank=True)

    class Meta:
        #managed = False
        db_table= 'equipment'

class Log(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('Accounts.User', on_delete=models.CASCADE,db_column='u_id' , related_name='log_user_id')
    model_name = models.ForeignKey('Equipment', on_delete=models.CASCADE, db_column='model_name')
    rent_count= models.IntegerField(default=0)
    return_deadline = models.DateTimeField(blank= True, null= True, default= None)
    rent_requested_date = models.DateTimeField(blank= True, null= True, default= None)
    rent_accepted_date = models.DateTimeField(blank= True, null= True, default= None, unique=True)
    return_requested_date = models.DateTimeField(blank= True, null= True, default= None)
    return_accepted_date = models.DateTimeField(blank= True, null= True, default= None, unique=True)
    rent_price= models.IntegerField(blank=True, null=True, default= None)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        #managed= False
        db_table = 'log'

class Renting(models.Model):
    user_id = models.ForeignKey('Accounts.User', on_delete=models.CASCADE, db_column='u_id',
                                related_name='renting_user_id')
    log_id = models.ForeignKey(Log, on_delete=models.CASCADE, db_column='log_id', related_name='renting_log_id', null=True)
    rent_accepted_date = models.ForeignKey(Log, on_delete=models.CASCADE, db_column='rent_accepted_date',
                                           to_field='rent_accepted_date', related_name='log_rent_date',
                                           null=True)

    class Meta:
        #managed= False
        db_table= 'renting'


class Returned(models.Model):
    log_id = models.ForeignKey(Log, on_delete=models.CASCADE, db_column='log_id', related_name='returned_log_id',
                               null=True)
    return_accepted_date = models.ForeignKey(Log, on_delete=models.CASCADE, db_column='return_accepted_date',
                                           to_field='return_accepted_date',
                                           null=True)
    class Meta:
        #managed=False
        db_table= 'returned'

class Returning(models.Model):
    log_id = models.ForeignKey(Log, on_delete=models.CASCADE, db_column='log_id', related_name='returning_log_id',
                               null=True)
    user_id = models.ForeignKey('Accounts.User', on_delete=models.CASCADE, db_column='u_id',
                                related_name='returning_user_id')

    class Meta:
        #managed=False
        db_table= 'returning'