# Generated by Django 3.2 on 2023-06-18 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_instagramuser_rewarded'),
    ]

    operations = [
        migrations.AddField(
            model_name='instagramuser',
            name='json',
            field=models.JSONField(blank=True, default=''),
        ),
    ]