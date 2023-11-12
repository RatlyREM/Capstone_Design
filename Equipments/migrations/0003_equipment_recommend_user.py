# Generated by Django 4.0.3 on 2023-11-12 17:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Equipments', '0002_alter_equipment_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='recommend_user',
            field=models.ManyToManyField(related_name='recommend_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
