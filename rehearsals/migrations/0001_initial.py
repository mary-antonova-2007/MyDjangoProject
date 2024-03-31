# Generated by Django 5.0.3 on 2024-03-31 08:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RehearsalDate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.IntegerField()),
                ('floor', models.IntegerField()),
                ('rehearsal_date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rehearsals.rehearsaldate')),
            ],
        ),
        migrations.CreateModel(
            name='Window',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_light_on', models.BooleanField()),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rehearsals.room')),
            ],
        ),
    ]