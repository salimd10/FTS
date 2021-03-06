# Generated by Django 2.0.7 on 2018-07-05 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FTS', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilesLogs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_id', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=30)),
                ('sender', models.CharField(default='', max_length=30)),
                ('receiver', models.CharField(default='', max_length=30)),
                ('action', models.CharField(default='', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='FileTracker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_id', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=30)),
                ('sender', models.CharField(default='', max_length=30)),
                ('receiver', models.CharField(default='', max_length=30)),
                ('status', models.CharField(default='', max_length=30)),
            ],
        ),
        migrations.RemoveField(
            model_name='file',
            name='description',
        ),
        migrations.RemoveField(
            model_name='file',
            name='destination',
        ),
        migrations.RemoveField(
            model_name='file',
            name='location',
        ),
        migrations.RemoveField(
            model_name='file',
            name='origin',
        ),
        migrations.RemoveField(
            model_name='file',
            name='status',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='email',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='phone',
        ),
    ]
