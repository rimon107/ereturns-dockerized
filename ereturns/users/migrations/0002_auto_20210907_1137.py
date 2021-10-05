# Generated by Django 3.1.13 on 2021-09-07 05:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institutes', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='approved_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_approved_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='approved_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='approved time'),
        ),
        migrations.AddField(
            model_name='user',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='institutes.branch'),
        ),
        migrations.AddField(
            model_name='user',
            name='change_approved_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_change_approved_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='institutes.department'),
        ),
        migrations.AddField(
            model_name='user',
            name='designation',
            field=models.CharField(blank=True, max_length=255, verbose_name='designation'),
        ),
        migrations.AddField(
            model_name='user',
            name='financial_institute',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='institutes.financialinstitute'),
        ),
        migrations.AddField(
            model_name='user',
            name='financial_institute_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='institutes.financialinstitutetype'),
        ),
        migrations.AddField(
            model_name='user',
            name='first_approved_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_first_approved_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
        migrations.AddField(
            model_name='user',
            name='last_password_update_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='approved time'),
        ),
        migrations.AddField(
            model_name='user',
            name='mobile',
            field=models.CharField(blank=True, max_length=255, verbose_name='mobile'),
        ),
        migrations.AddField(
            model_name='user',
            name='password_reset_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='approved time'),
        ),
        migrations.AddField(
            model_name='user',
            name='password_updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_password_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=255, verbose_name='phone'),
        ),
        migrations.AddField(
            model_name='user',
            name='random_string',
            field=models.CharField(blank=True, max_length=255, verbose_name='random string'),
        ),
        migrations.AddField(
            model_name='user',
            name='report_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='institutes.reporttype'),
        ),
        migrations.AddField(
            model_name='user',
            name='second_approved_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_second_approved_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.IntegerField(choices=[(1, 'Online'), (0, 'Offline')], default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, max_length=255, verbose_name='name'),
        ),
    ]
