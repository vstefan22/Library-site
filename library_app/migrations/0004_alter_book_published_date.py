# Generated by Django 4.1 on 2022-08-21 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0003_book_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='published_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]