# Generated by Django 5.1.1 on 2024-09-29 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather_web', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
