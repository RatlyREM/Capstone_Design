from django.db import models
from django.utils import timezone
import Accounts.models

class BoardModel(models.Model):
    user_id = models.ForeignKey('Accounts.User', on_delete=models.CASCADE, db_column='u_id',
                                related_name='board_user_id')
    written_date = models.DateTimeField(auto_now_add=True)
    title= models.CharField(max_length=100, blank=True)
    field= models.CharField(max_length=500)
    answer= models.CharField(max_length=500, null=True, default= None)
    hit_count = models.IntegerField(blank=True, default=0)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        #managed= False
        db_table = 'board'
