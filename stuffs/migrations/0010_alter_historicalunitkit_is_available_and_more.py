# Generated by Django 4.2.5 on 2024-08-27 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stuffs', '0009_historicalunitkit_is_available_unitkit_is_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalunitkit',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='unitkit',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
    ]
