# Generated by Django 3.2.4 on 2022-03-11 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmsapp', '0042_remove_request_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='email',
            field=models.CharField(default=None, max_length=20, null=True),
        ),
    ]
