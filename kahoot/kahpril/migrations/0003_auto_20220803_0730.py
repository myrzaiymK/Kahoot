# Generated by Django 3.2 on 2022-08-03 07:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kahpril', '0002_auto_20220803_0526'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'ordering': ['-rating']},
        ),
        migrations.RenameField(
            model_name='customuser',
            old_name='passed_tests',
            new_name='tests',
        ),
    ]