# Generated by Django 3.1.2 on 2020-10-15 14:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('worktime', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='dateFrom',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Beginn'),
        ),
    ]