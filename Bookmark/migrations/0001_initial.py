# Generated by Django 4.0.3 on 2023-11-24 13:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Equipments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.ForeignKey(db_column='model_name', on_delete=django.db.models.deletion.CASCADE, related_name='bookmark_model_name', to='Equipments.equipment')),
                ('user_id', models.ForeignKey(db_column='u_id', on_delete=django.db.models.deletion.CASCADE, related_name='bookmark_user_id', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'favorites',
            },
        ),
    ]
