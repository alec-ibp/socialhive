# Generated by Django 4.2.1 on 2023-06-04 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_alter_historicalhiveuser_password_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalhiveuser',
            name='role',
            field=models.IntegerField(choices=[(1, 'Admin'), (2, 'User')], default=2),
        ),
        migrations.AddField(
            model_name='hiveuser',
            name='role',
            field=models.IntegerField(choices=[(1, 'Admin'), (2, 'User')], default=2),
        ),
    ]