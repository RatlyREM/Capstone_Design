from django.db import models
from django.utils import timezone

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

    recommend_user = models.ManyToManyField(Accounts.models.User, related_name='recommend_user', blank=True)

    class Meta:
        #managed = False
        db_table= 'equipment'