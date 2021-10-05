# Generated by Django 3.1.13 on 2021-09-12 05:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import ereturns.common.file_upload


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('institutes', '0001_initial'),
        ('rit', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ritmanagement',
            name='base_date',
        ),
        migrations.RemoveField(
            model_name='ritmanagement',
            name='branch',
        ),
        migrations.RemoveField(
            model_name='ritmanagement',
            name='financial_institute',
        ),
        migrations.AddField(
            model_name='ritmanagement',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='institutes.department'),
        ),
        migrations.AddField(
            model_name='ritmanagement',
            name='file_type',
            field=models.IntegerField(choices=[(1, 'RIT'), (2, 'Reference File'), (2, 'User Manual'), (2, 'User Registration Form')], default=1),
        ),
        migrations.AddField(
            model_name='ritmanagement',
            name='upload_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='upload time'),
        ),
        migrations.AddField(
            model_name='ritmanagement',
            name='uploaded_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rit_mgt_uploaded_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ritmanagement',
            name='version',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='version'),
        ),
        migrations.AlterField(
            model_name='ritmanagement',
            name='file',
            field=models.FileField(upload_to=ereturns.common.file_upload.directory_path),
        ),
        migrations.AlterField(
            model_name='ritmanagement',
            name='rit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rit.ritfeatures'),
        ),
        migrations.AlterField(
            model_name='ritsupervision',
            name='file',
            field=models.FileField(upload_to=ereturns.common.file_upload.rit_directory_path),
        ),
    ]
