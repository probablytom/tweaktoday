# Generated by Django 3.0.4 on 2020-03-22 18:54

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskSuggestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_text', models.CharField(max_length=200)),
                ('option_explainer', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Tweak',
            fields=[
                ('tasksuggestion_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tt_core.TaskSuggestion')),
            ],
            bases=('tt_core.tasksuggestion',),
        ),
        migrations.AddField(
            model_name='tasksuggestion',
            name='option_voters',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tt_core.User'),
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tweak_url', models.URLField(default='', max_length=1000)),
                ('submission_explainer', models.CharField(default='', max_length=2000)),
                ('submitted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tt_core.User')),
                ('tweak_submitted_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tt_core.Tweak')),
            ],
        ),
    ]