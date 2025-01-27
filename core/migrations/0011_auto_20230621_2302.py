# Generated by Django 3.2 on 2023-06-22 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_instagramuser_rewarded_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='instagramuser',
            name='token',
            field=models.CharField(max_length=6, null=True, verbose_name='Token de verificacao'),
        ),
        migrations.AlterField(
            model_name='instagramuser',
            name='user_name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Nome de Usuario'),
        ),
    ]
