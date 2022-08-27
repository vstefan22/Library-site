# Generated by Django 4.1 on 2022-08-27 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0006_savedbook'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='savedbook',
            name='book',
        ),
        migrations.AddField(
            model_name='savedbook',
            name='title',
            field=models.CharField(default='', max_length=100),
        ),
    ]