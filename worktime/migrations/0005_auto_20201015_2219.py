# Generated by Django 3.1.2 on 2020-10-15 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worktime', '0004_auto_20201015_2216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='type',
            field=models.CharField(choices=[], max_length=255, verbose_name='Typ'),
        ),
    ]
