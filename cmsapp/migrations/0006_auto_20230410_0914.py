# Generated by Django 3.2.4 on 2023-04-10 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmsapp', '0005_auto_20221004_0949'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='correction',
            field=models.TextField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='request',
            name='documents',
            field=models.TextField(max_length=1000, null=True),
        ),
    ]