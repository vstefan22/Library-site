# Generated by Django 3.2.9 on 2022-08-26 14:20

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', models.ImageField(blank=True, default='Nana.jpg', null=True, upload_to='images/')),
                ('description', models.TextField(blank=True, max_length=950, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('read_books_count', models.IntegerField(blank=True, default=0, null=True)),
                ('read_books_list', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=100, null=True), blank=True, null=True, size=None)),
                ('profile', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, default='Nana.jpg', null=True, upload_to='images/')),
                ('title', models.CharField(max_length=150, unique=True)),
                ('author', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=5000, null=True)),
                ('published_date', models.DateField(blank=True, null=True)),
                ('language', models.CharField(blank=True, default='Not selected', max_length=100, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AddReadBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('describe', models.TextField()),
                ('started_reading', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
