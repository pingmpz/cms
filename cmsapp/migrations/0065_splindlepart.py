# Generated by Django 3.2.4 on 2022-05-13 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmsapp', '0064_auto_20220513_1359'),
    ]

    operations = [
        migrations.CreateModel(
            name='SplindlePart',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('machine', models.CharField(max_length=100, null=True)),
                ('model', models.CharField(max_length=100, null=True)),
                ('amount', models.IntegerField(default=0)),
                ('register_date', models.DateField(null=True)),
                ('marker', models.CharField(max_length=100, null=True)),
                ('serial_no', models.CharField(max_length=100, null=True)),
                ('nose', models.CharField(max_length=100, null=True)),
                ('max_speed', models.CharField(max_length=100, null=True)),
                ('drive_type', models.CharField(max_length=100, null=True)),
                ('lubrication', models.CharField(max_length=100, null=True)),
                ('condition', models.CharField(max_length=100, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
