# Generated by Django 3.2.6 on 2022-06-03 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20220529_0159'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='level',
            new_name='exp_sum',
        ),
    ]
