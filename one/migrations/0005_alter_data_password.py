# Generated by Django 3.2.5 on 2021-07-22 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('one', '0004_alter_data_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='password',
            field=models.TextField(),
        ),
    ]