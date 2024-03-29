# Generated by Django 3.1.3 on 2021-01-14 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0002_auto_20210110_0415'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='NewsSource',
            new_name='newsSource',
        ),
        migrations.RenameField(
            model_name='article',
            old_name='Paywall',
            new_name='paywall',
        ),
        migrations.RenameField(
            model_name='article',
            old_name='Summary',
            new_name='summary',
        ),
        migrations.RenameField(
            model_name='article',
            old_name='Title',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='article',
            old_name='Url',
            new_name='url',
        ),
        migrations.RenameField(
            model_name='newssource',
            old_name='NewsSourceData',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='newssource',
            old_name='NewsSource',
            new_name='newsSource',
        ),
        migrations.RenameField(
            model_name='newssource',
            old_name='Paywall',
            new_name='paywall',
        ),
        migrations.AddField(
            model_name='newssource',
            name='homepage',
            field=models.URLField(default='www.google.com', max_length=100),
        ),
    ]
