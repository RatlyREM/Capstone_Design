# Generated by Django 4.0.3 on 2023-11-24 18:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Equipments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='returned',
            name='user_id',
            field=models.ForeignKey(db_column='u_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='returned_user_id', to=settings.AUTH_USER_MODEL),
        ),
    ]
