# Generated by Django 4.2.1 on 2023-06-11 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0002_post_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
