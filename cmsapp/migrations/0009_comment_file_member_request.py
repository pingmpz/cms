# Generated by Django 3.2.4 on 2022-03-06 16:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cmsapp', '0008_alter_machine_section'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('req_no', models.CharField(max_length=10)),
                ('emp_id', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=100)),
                ('section', models.CharField(max_length=10)),
                ('phone_no', models.CharField(max_length=10)),
                ('req_to', models.CharField(max_length=10)),
                ('request_date', models.DateField(null=True)),
                ('status', models.CharField(max_length=20)),
                ('reason', models.CharField(max_length=1000, null=True)),
                ('description', models.CharField(max_length=1000)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('mc', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cmsapp.machine')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('req', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmsapp.request')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('req', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmsapp.request')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('req', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmsapp.request')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]