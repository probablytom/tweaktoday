# Generated by Django 3.0.4 on 2020-03-22 19:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tt_core', '0004_auto_20200322_1907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasksuggestion',
            name='task_voters',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
