from django.db import models
from django.utils import timezone
from datetime import datetime

import Accounts.models
import Equipments.models


class Favorites(models.Model):
    model_name = models.ForeignKey('Equipments.Equipment', on_delete=models.CASCADE, db_column='model_name', related_name='bookmark_model_name')
    user_id = models.ForeignKey('Accounts.User', on_delete=models.CASCADE, db_column='u_id', related_name='bookmark_user_id')
    class Meta:
        #managed= False
        db_table = 'favorites'
