# Generated by Django 3.0.4 on 2020-03-28 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tt_core', '0013_auto_20200328_1359'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='sumbission',
            new_name='submission',
        ),
        migrations.AlterField(
            model_name='comment',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
