# Generated by Django 3.2 on 2022-08-03 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kahpril', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='player_passed',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='quiz',
            name='questions_count',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]