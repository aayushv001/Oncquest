# Generated by Django 3.2.5 on 2021-07-26 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('one', '0008_auto_20210725_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdata',
            name='runstat',
            field=models.CharField(default='ER', max_length=2),
            preserve_default=False,
        ),
    ]
