# Generated by Django 3.2 on 2023-06-18 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20230617_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instagramuser',
            name='rewarded',
            field=models.BooleanField(blank=True, default=False, verbose_name='Recompensado'),
        ),
    ]