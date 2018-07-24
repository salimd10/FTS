# Generated by Django 2.0.7 on 2018-07-11 15:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('FTS', '0004_auto_20180705_1911'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileslogs',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='department',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='file',
            name='file_id',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='file',
            name='name',
            field=models.CharField(max_length=400),
        ),
        migrations.AlterField(
            model_name='fileslogs',
            name='file_id',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='fileslogs',
            name='name',
            field=models.CharField(max_length=400),
        ),
        migrations.AlterField(
            model_name='filetracker',
            name='file_id',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='filetracker',
            name='name',
            field=models.CharField(default='', max_length=400),
        ),
        migrations.AlterField(
            model_name='office',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='stafflogin',
            name='password',
            field=models.CharField(default='password', max_length=20),
        ),
    ]
