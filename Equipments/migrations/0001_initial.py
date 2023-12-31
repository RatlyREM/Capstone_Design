# Generated by Django 4.0.3 on 2023-11-24 13:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('model_name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(default=None, max_length=30)),
                ('type', models.CharField(default=None, max_length=30)),
                ('price', models.IntegerField(blank=True, default=0, null=True)),
                ('repository', models.CharField(default=None, max_length=30)),
                ('total_rent', models.IntegerField(blank=True, default=0, null=True)),
                ('total_stock', models.IntegerField(blank=True, default=0, null=True)),
                ('current_stock', models.IntegerField(blank=True, default=0, null=True)),
                ('manufacturer', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('recommend_count', models.IntegerField(blank=True, default=0, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('recommend_user', models.ManyToManyField(blank=True, related_name='recommend_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'equipment',
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('rent_count', models.IntegerField(default=0)),
                ('return_deadline', models.DateTimeField(blank=True, default=None, null=True)),
                ('rent_requested_date', models.DateTimeField(blank=True, default=None, null=True)),
                ('rent_accepted_date', models.DateTimeField(blank=True, default=None, null=True, unique=True)),
                ('return_requested_date', models.DateTimeField(blank=True, default=None, null=True)),
                ('return_accepted_date', models.DateTimeField(blank=True, default=None, null=True, unique=True)),
                ('rent_price', models.IntegerField(blank=True, default=None, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('model_name', models.ForeignKey(db_column='model_name', on_delete=django.db.models.deletion.CASCADE, to='Equipments.equipment')),
                ('user_id', models.ForeignKey(db_column='u_id', on_delete=django.db.models.deletion.CASCADE, related_name='log_user_id', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'log',
            },
        ),
        migrations.CreateModel(
            name='Returning',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_id', models.ForeignKey(db_column='log_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='returning_log_id', to='Equipments.log')),
                ('user_id', models.ForeignKey(db_column='u_id', on_delete=django.db.models.deletion.CASCADE, related_name='returning_user_id', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'returning',
            },
        ),
        migrations.CreateModel(
            name='Returned',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_id', models.ForeignKey(db_column='log_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='returned_log_id', to='Equipments.log')),
                ('return_accepted_date', models.ForeignKey(db_column='return_accepted_date', null=True, on_delete=django.db.models.deletion.CASCADE, to='Equipments.log', to_field='return_accepted_date')),
            ],
            options={
                'db_table': 'returned',
            },
        ),
        migrations.CreateModel(
            name='Renting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_id', models.ForeignKey(db_column='log_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='renting_log_id', to='Equipments.log')),
                ('rent_accepted_date', models.ForeignKey(db_column='rent_accepted_date', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='log_rent_date', to='Equipments.log', to_field='rent_accepted_date')),
                ('user_id', models.ForeignKey(db_column='u_id', on_delete=django.db.models.deletion.CASCADE, related_name='renting_user_id', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'renting',
            },
        ),
    ]
