# Generated by Django 3.1.4 on 2020-12-25 01:35

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('year', models.IntegerField(default=0)),
                ('level', models.CharField(choices=[('R', 'Regionals'), ('P', 'Provincials'), ('I', 'ICDC')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Cluster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('audio_file', models.FileField(upload_to='case/audio/')),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roleplay.case')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=10)),
                ('team', models.BooleanField(default=False)),
                ('cluster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roleplay.cluster')),
            ],
        ),
        migrations.AddField(
            model_name='case',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roleplay.event'),
        ),
    ]
