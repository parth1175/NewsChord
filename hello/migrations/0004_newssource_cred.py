# Generated by Django 3.1.3 on 2021-01-26 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0003_auto_20210114_0137'),
    ]

    operations = [
        migrations.AddField(
            model_name='newssource',
            name='cred',
            field=models.CharField(default='n/a', max_length=200),
        ),
    ]
