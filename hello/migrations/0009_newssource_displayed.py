# Generated by Django 3.1.3 on 2021-06-02 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0008_remove_article_tempignore'),
    ]

    operations = [
        migrations.AddField(
            model_name='newssource',
            name='displayed',
            field=models.BooleanField(default=True),
        ),
    ]
