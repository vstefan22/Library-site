# Generated by Django 4.1 on 2022-08-22 12:38

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0005_person'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='read_books_list',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=100), size=None), size=None),
        ),
    ]