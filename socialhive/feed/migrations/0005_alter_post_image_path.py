# Generated by Django 4.2.1 on 2023-06-11 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0004_alter_post_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image_path',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
