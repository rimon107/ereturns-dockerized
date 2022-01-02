# Generated by Django 3.1.13 on 2021-12-05 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20211109_1210'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='report_type',
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
    ]
