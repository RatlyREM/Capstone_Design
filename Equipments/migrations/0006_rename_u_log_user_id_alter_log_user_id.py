# Generated by Django 4.0.3 on 2023-11-22 14:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Equipments', '0005_alter_log_table'),
    ]

    operations = [
        migrations.RenameField(
            model_name='log',
            old_name='u',
            new_name='user_id',
        ),
        migrations.AlterField(
            model_name='log',
            name='user_id',
            field=models.ForeignKey(db_column='u_id', on_delete=django.db.models.deletion.CASCADE, related_name='log_user_id', to=settings.AUTH_USER_MODEL),
        ),
    ]
