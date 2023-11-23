# Generated by Django 4.0.3 on 2023-11-23 22:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Equipments', '0002_renting_rent_accepted_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='renting',
            name='rent_accepted_date',
            field=models.ForeignKey(db_column='rent_accepted_date', null=True, on_delete=django.db.models.deletion.CASCADE, to='Equipments.log', to_field='rent_accepted_date'),
        ),
    ]
