# Generated by Django 3.2.5 on 2021-07-25 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('one', '0006_pdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdata',
            name='srfid',
            field=models.BigIntegerField(unique=True),
        ),
    ]
