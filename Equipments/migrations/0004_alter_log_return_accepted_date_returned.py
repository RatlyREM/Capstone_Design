# Generated by Django 4.0.3 on 2023-11-23 22:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Equipments', '0003_alter_renting_rent_accepted_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='return_accepted_date',
            field=models.DateTimeField(blank=True, default=None, null=True, unique=True),
        ),
        migrations.CreateModel(
            name='Returned',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_id', models.ForeignKey(db_column='log_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='returned_log_id', to='Equipments.log')),
                ('return_accepted_date', models.ForeignKey(db_column='return_accepted_date', null=True, on_delete=django.db.models.deletion.CASCADE, to='Equipments.log', to_field='return_accepted_date')),
            ],
        ),
    ]
