# Generated by Django 3.2.5 on 2021-08-02 06:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('one', '0011_regdata'),
    ]

    operations = [
        migrations.RenameField(
            model_name='regdata',
            old_name='Address',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='regdata',
            old_name='Age',
            new_name='age',
        ),
        migrations.RenameField(
            model_name='regdata',
            old_name='Gender',
            new_name='gender',
        ),
    ]
