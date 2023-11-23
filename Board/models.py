from django.db import models
from django.utils import timezone
from datetime import datetime

import Accounts.models
import Equipments.models

class BoardModel(models.Model):
    user_id = models.ForeignKey('Accounts.User', on_delete=models.CASCADE, db_column='u_id',
                                related_name='board_user_id')
    written_date = models.DateTimeField(auto_now_add=True)
    title= models.CharField(max_length=100, blank=True, null=True, default='No title')
    field= models.CharField(max_length=500)
    answer= models.CharField(max_length=500, blank=True, null=True, default= None)
    hit_count = models.IntegerField(blank=True, default=0)
    class Meta:
        #managed= False
        db_table = 'board'
