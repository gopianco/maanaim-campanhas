# Generated by Django 3.2 on 2023-06-23 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20230621_2302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instagramuser',
            name='post_id',
            field=models.CharField(max_length=500, verbose_name='Id do post'),
        ),
        migrations.AlterField(
            model_name='instagramuser',
            name='user_name',
            field=models.CharField(max_length=500, unique=True, verbose_name='Nome de Usuario'),
        ),
    ]