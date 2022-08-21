# Generated by Django 3.2.9 on 2022-08-21 16:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, default='Nana.jpg', null=True, upload_to='images/')),
                ('title', models.CharField(max_length=150)),
                ('author', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=5000, null=True)),
                ('published_date', models.DateField(blank=True, default='Unknown', null=True)),
                ('read', models.BooleanField(default=False)),
                ('started_reading', models.DateField(blank=True, null=True)),
                ('finished_reading', models.DateField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
