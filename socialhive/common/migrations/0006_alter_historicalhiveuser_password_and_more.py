# Generated by Django 4.2.1 on 2023-06-04 16:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_alter_historicalhiveuser_username_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalhiveuser',
            name='password',
            field=models.CharField(max_length=265, validators=[django.core.validators.MinLengthValidator(8), django.core.validators.MaxLengthValidator(265)]),
        ),
        migrations.AlterField(
            model_name='hiveuser',
            name='password',
            field=models.CharField(max_length=265, validators=[django.core.validators.MinLengthValidator(8), django.core.validators.MaxLengthValidator(265)]),
        ),
    ]
