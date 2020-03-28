# Generated by Django 3.0.4 on 2020-03-28 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tt_core', '0012_submission_submission_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='is_video',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AddField(
            model_name='submission',
            name='mime',
            field=models.CharField(default='photo/jpeg', max_length=30),
        ),
    ]