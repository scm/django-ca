# Generated by Django 3.1.3 on 2020-12-06 12:53

from django.db import migrations, models
import django_ca.models


class Migration(migrations.Migration):

    dependencies = [
        ('django_ca', '0037_auto_20201206_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acmechallenge',
            name='token',
            field=models.CharField(blank=True, default=django_ca.models.acme_token, max_length=64),
        ),
    ]