# Generated by Django 3.0.8 on 2020-07-18 09:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myAuth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='texts',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 7, 18, 9, 38, 54, 379223)),
        ),
    ]
